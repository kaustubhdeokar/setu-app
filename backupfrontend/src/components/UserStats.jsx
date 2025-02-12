import React, { useState, useEffect } from 'react';
import {getAnalyticsEntries} from '../services/User'

export default function UserStats() {

  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await getAnalyticsEntries();
        if(response.status === 401){
          localStorage.removeItem('token');
          navigate('/');
        }
        setStats(response.data);
        setLoading(false);
      } catch (err) {
        setError("Failed to load user statistics");
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  if (loading) {
    return <div className="p-4">Loading user statistics...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">{error}</div>;
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">User Statistics</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-300">
          <thead className="bg-gray-100">
            <tr>
              <th className="border p-2 text-left">ID</th>
              <th className="border p-2 text-left">Username</th>
              <th className="border p-2 text-left">KYC Pass</th>
              <th className="border p-2 text-left">KYC Fail</th>
              <th className="border p-2 text-left">Bank Pass</th>
              <th className="border p-2 text-left">Bank Fail</th>
              <th className="border p-2 text-left">Total Pass</th>
              <th className="border p-2 text-left">Total Fail</th>
            </tr>
          </thead>
          <tbody>
            {stats.map((stat) => (
              <tr key={stat.id}>
                <td className="border p-2">{stat.id}</td>
                <td className="border p-2">{stat.username}</td>
                <td className="border p-2">{stat.pass_kyc}</td>
                <td className="border p-2">{stat.fail_kyc}</td>
                <td className="border p-2">{stat.pass_bank}</td>
                <td className="border p-2">{stat.fail_bank}</td>
                <td className="border p-2">{stat.total_pass}</td>
                <td className="border p-2">{stat.fail_bank}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
