import React from "react";
import { useNavigate } from "react-router-dom";
import { makePaymentRequest, fetchBankDetails, updateAnalytics } from "../services/PaymentService";
import { useState } from "react";
const PaymentInit = ({ onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handlePaymentInitiation = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await makePaymentRequest();
      if (response.data.status === 200) {
        const bankData = {
          requestId: response.data.request_id,
          bankAccount: response.data.bank_account,
          ifsc: response.data.ifsc,
        };

        const verificationResult = await handleBankVerification(
          bankData.requestId,
          bankData.bankAccount,
          bankData.ifsc
        );

        if (verificationResult) {
          onSuccess(bankData);
        }
      } else if (response.status === 401) {
        localStorage.removeItem("token");
        navigate("/");
      } else {
        throw new Error("Payment initiation failed");
      }
    } catch (error) {
      setError(error.message || "Error in payment initiation");
    }
    setLoading(false);
  };

  const handleBankVerification = async (requestId, bankAccount, ifsc) => {
    try {
        const response = await fetchBankDetails(requestId);
        if (
        response.data.bank_account === bankAccount &&
        response.data.ifsc === ifsc
      ) {
        // updateAnalytics(localStorage.getItem("user")); done through backend.
        return true;
      } else if (response.status === 401) {
        localStorage.removeItem("token");
        navigate("/");
        return false;
      } else {
        throw new Error("Bank account verification failed");
      }
    } catch (error) {
      setError(error.message || "Error verifying bank details");
      return false;
    }
  };

  return (
    <div>
        {error && (
            <div className="mb-4 text-red-500 p-2 bg-red-50 rounded">{error}</div>
        )}

        <button
            onClick={handlePaymentInitiation}
            disabled={loading}
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300">
        {loading ? "Processing..." : "Initiate ₹1 Payment"}
        </button>
    </div>
    );
};

export default PaymentInit;
