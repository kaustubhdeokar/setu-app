import React, { useReducer, useState } from "react";
import { verifyPan } from "../services/PanService";
import { useNavigate } from 'react-router-dom';
import {
  makePaymentRequest,
  fetchBankDetails,
} from "../services/MockPaymentService";

const STEPS = {
  PAN_VALIDATION: "PAN_VALIDATION",
  PAYMENT_INITIATION: "PAYMENT_INITIATION",
  PAYMENT_VERIFICATION: "PAYMENT_VERIFICATION",
  COMPLETED: "COMPLETED",
};

const ACTIONS = {
  SET_LOADING: "SET_LOADING",
  SET_ERROR: "SET_ERROR",
  SET_SUCCESS: "SET_SUCCESS",
  UPDATE_DATA: "UPDATE_DATA",
  RESET: "RESET",
};

const initialState = {
  currentStep: STEPS.PAN_VALIDATION,
  loading: false,
  error: null,
  data: {
    pan: "",
    fullName: "",
    requestId: "",
    bankAccount: "",
    ifsc: "",
  },
};

function kycReducer(state, action) {
  switch (action.type) {
    case ACTIONS.SET_LOADING:
      return { ...state, loading: action.payload, error: null };
    case ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        loading: false,
        currentStep: action.resetStep
          ? STEPS.PAN_VALIDATION
          : state.currentStep,
      };
    case ACTIONS.SET_SUCCESS:
      return {
        ...state,
        currentStep: action.payload,
        loading: false,
        error: null,
      };
    case ACTIONS.UPDATE_DATA:
      return {
        ...state,
        data: { ...state.data, ...action.payload },
      };
    case ACTIONS.RESET:
      return initialState;
    default:
      return state;
  }
}

const stepConfig = {
  [STEPS.PAN_VALIDATION]: {
    title: "PAN Validation",
    buttonText: "Validate PAN",
    loadingText: "Validating...",
  },
  [STEPS.PAYMENT_INITIATION]: {
    title: "Payment Initiation",
    buttonText: "Initiate ₹1 Payment",
    loadingText: "Processing...",
  },
  [STEPS.PAYMENT_VERIFICATION]: {
    title: "Payment Verification",
    buttonText: "Verify Payment",
    loadingText: "Verifying...",
  },
  [STEPS.COMPLETED]: {
    title: "Completed",
  },
};

export default function KYCValidation() {
  const [state, dispatch] = useReducer(kycReducer, initialState);
  const [pan, setPan] = useState("");
  const navigate = useNavigate();

  const handlePanValidation = async () => {
    dispatch({ type: ACTIONS.SET_LOADING, payload: true });
    try {
      const response = await verifyPan(pan);
      if (response.data.status === 200) {
        dispatch({
          type: ACTIONS.UPDATE_DATA,
          payload: {
            pan,
            fullName: response.data.full_name,
          },
        });
        dispatch({
          type: ACTIONS.SET_SUCCESS,
          payload: STEPS.PAYMENT_INITIATION,
        });
      } 
      else if(response.status === 401){
        localStorage.removeItem('token');
        navigate('/');
      }
      else {
        throw new Error("Invalid PAN card number");
      }
    } catch (error) {
      dispatch({
        type: ACTIONS.SET_ERROR,
        payload: error.message || "Error validating PAN",
      });
    }
  };

  const handlePaymentInitiation = async () => {
    dispatch({ type: ACTIONS.SET_LOADING, payload: true });
    try {
      const response = await makePaymentRequest();
      if (response.data.status === 200) {
        dispatch({
          type: ACTIONS.UPDATE_DATA,
          payload: {
            requestId: response.data.request_id,
            bankAccount: response.data.bank_account,
            ifsc: response.data.ifsc,
          },
        });
        await handleBankVerification(
          response.data.request_id,
          response.data.bank_account,
          response.data.ifsc
        );
      } 
      else if(response.status === 401){
        localStorage.removeItem('token');
        navigate('/');
      }
      else {
        throw new Error("Payment initiation failed");
      }
    } catch (error) {
      dispatch({
        type: ACTIONS.SET_ERROR,
        payload: error.message || "Error in payment initiation",
        resetStep: true,
      });
    }
  };

  const handleBankVerification = async (requestId, bankAccount, ifsc) => {
    try {
      const response = await fetchBankDetails(requestId);
      if (
        response.data.bank_account === bankAccount &&
        response.data.ifsc === ifsc
      ) {
        dispatch({ type: ACTIONS.SET_SUCCESS, payload: STEPS.COMPLETED });
      }
      else if(response.status === 401){
        localStorage.removeItem('token');
        navigate('/');
      }
      else {
        throw new Error("Bank account verification failed");
      }
    } catch (error) {
      dispatch({
        type: ACTIONS.SET_ERROR,
        payload: error.message || "Error verifying bank details",
        resetStep: true,
      });
    }
  };

  const currentStepConfig = stepConfig[state.currentStep];

  const handleStepAction = () => {
    switch (state.currentStep) {
      case STEPS.PAN_VALIDATION:
        return handlePanValidation();
      case STEPS.PAYMENT_INITIATION:
        return handlePaymentInitiation();
      default:
        return null;
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-semibold mb-4">
        KYC Validation - {currentStepConfig.title}
      </h2>

      {state.data.fullName && (
        <div className="mb-4 text-gray-700">Hello, {state.data.fullName}!</div>
      )}

      {state.error && (
        <div className="mb-4 text-red-500 p-2 bg-red-50 rounded">
          {state.error}
        </div>
      )}

      {state.currentStep === STEPS.PAN_VALIDATION && (
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Enter PAN Card Number"
            value={pan}
            onChange={(e) => setPan(e.target.value.toUpperCase())}
            className="border p-2 w-full rounded"
            maxLength={10}
          />
        </div>
      )}

      {state.currentStep !== STEPS.COMPLETED && (
        <button
          onClick={handleStepAction}
          disabled={state.loading}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
        >
          {state.loading
            ? currentStepConfig.loadingText
            : currentStepConfig.buttonText}
        </button>
      )}

      {state.currentStep === STEPS.COMPLETED && (
        <div className="text-green-600 font-semibold">
          ✅ KYC Validation & Mock Payment Successful!
          <div className="mt-2 text-sm text-gray-600">
            Bank Account: {state.data.bankAccount}
            <br />
            IFSC: {state.data.ifsc}
          </div>
        </div>
      )}
    </div>
  );
}
