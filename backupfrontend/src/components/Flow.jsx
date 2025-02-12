import React from "react";
import { useState } from "react";
import PanValidation from "./PanValidation";
import PaymentInit from "./PaymentInit.jsx";
import { STEPS } from "../config/constants.js";

function Flow() {
  const [currentStep, setCurrentStep] = useState(STEPS.PAN_VALIDATION);
  const [userData, setUserData] = useState({
    fullName: "",
    bankAccount: "",
    ifsc: "",
  });

  const handlePanSuccess = (panData) => {
    setUserData((prev) => ({ ...prev, fullName: panData.fullName }));
    setCurrentStep(STEPS.PAYMENT_INITIATION);
  };

  const handlePaymentSuccess = (bankData) => {
    setUserData((prev) => ({
      ...prev,
      bankAccount: bankData.bankAccount,
      ifsc: bankData.ifsc,
    }));
    setCurrentStep(STEPS.COMPLETED);
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-semibold mb-4">
        KYC Validation -{" "}
        {currentStep === STEPS.COMPLETED
        ? "Completed"
        : currentStep === STEPS.PAYMENT_INITIATION
        ? "Payment Initiation"
        : "PAN Validation"}
    </h2>

    {userData.fullName && (
        <div className="mb-4 text-gray-700">Hello, {userData.fullName}!</div>
    )}

    {currentStep === STEPS.PAN_VALIDATION && (
        <PanValidation onSuccess={handlePanSuccess} />
    )}

    {currentStep === STEPS.PAYMENT_INITIATION && (
        <PaymentInit onSuccess={handlePaymentSuccess} />
    )}

    {currentStep === STEPS.COMPLETED && (
        <div className="text-green-600 font-semibold">
        ✅ KYC Validation & Mock Payment Successful!
        <div className="mt-2 text-sm text-gray-600">
            Bank Account: {userData.bankAccount}
            <br />
            IFSC: {userData.ifsc}
        </div>
        </div>
    )}
    </div>
);
}

export default Flow;
