import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyPan } from "../services/PanService";
const PanValidation = ({ onSuccess }) => {
  const [pan, setPan] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handlePanValidation = async () => {
     
    setLoading(true);
    setError(null);
    try {
      const response = await verifyPan(pan);
      if (response.data.status === 200) {
        onSuccess({
          pan,
          fullName: response.data.full_name,
        });
      } else if (response.status === 401) {
        localStorage.removeItem("token");
        navigate("/");
      } else {
        throw new Error("Invalid PAN card number");
      }
    } catch (error) {
      setError(error.message || "Error validating PAN");
    }
    setLoading(false);
  };

  return (
    <div>
      {error && (
        <div className="mb-4 text-red-500 p-2 bg-red-50 rounded">{error}</div>
      )}

      <div className="space-y-4">
        <input
          type="text"
          placeholder="Enter PAN Card Number"
          value={pan}
          onChange={(e) => setPan(e.target.value.toUpperCase())}
          className="border p-2 w-full rounded"
          maxLength={10}
        />
        <button
          onClick={handlePanValidation}
          disabled={loading}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
        >
          {loading ? "Validating..." : "Validate PAN"}
        </button>
      </div>
    </div>
  );
}

export default PanValidation;
