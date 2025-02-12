

export const STEPS = {
  PAN_VALIDATION: "PAN_VALIDATION",
  PAYMENT_INITIATION: "PAYMENT_INITIATION",
  PAYMENT_VERIFICATION: "PAYMENT_VERIFICATION",
  COMPLETED: "COMPLETED",
};

export const stepConfig = {
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
