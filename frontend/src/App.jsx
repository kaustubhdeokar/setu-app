import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import KYCValidation from './components/KYCValidation'
function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100 py-8">
    <div className="container mx-auto">
      <h1 className="text-2xl font-bold text-center mb-8">KYC Verification Portal</h1>
      <KYCValidation />
    </div>
  </div>
  )
}

export default App
