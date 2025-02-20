"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Package, LogOut } from "lucide-react"
import { useNavigate, Link } from "react-router-dom"

import InventoryList from "./InventoryList"
import StockAlerts from "./StockAlerts"
import BatchTracking from "./BatchTracking"
import SupplierIntegration from "./SupplierIntegration"
import Analytics from "./Analytics"

const HomePage: React.FC = () => {
  const [inventory, setInventory] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch("http://localhost:8000/products")
        const data = await response.json()
        setInventory(data)
      } catch (error) {
        console.error("Error fetching products:", error)
      }
    }

    fetchProducts()
    const interval = setInterval(fetchProducts, 5000) // Fetch every 5 seconds
    return () => clearInterval(interval) // Cleanup on unmount
  }, [])

  const handleLogout = () => {
    navigate("/")
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-600 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center">
            <Package className="w-8 h-8 mr-2" />
            <h1 className="text-2xl font-bold">Merchandise Inventory Manager</h1>
          </div>
          <button onClick={handleLogout} className="flex items-center bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded">
            <LogOut className="w-5 h-5 mr-2" />
            Logout
          </button>
        </div>
      </nav>
      <div className="container mx-auto p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Link to="/inventory" className="bg-white shadow-md rounded-lg p-4 hover:shadow-lg transition-shadow">
            <InventoryList inventory={inventory} />
          </Link>
          <Link to="/alerts" className="bg-white shadow-md rounded-lg p-4 hover:shadow-lg transition-shadow">
            <StockAlerts inventory={inventory} />
          </Link>
          <Link to="/batches" className="bg-white shadow-md rounded-lg p-4 hover:shadow-lg transition-shadow">
            <BatchTracking inventory={inventory} />
          </Link>
          <Link to="/suppliers" className="bg-white shadow-md rounded-lg p-4 hover:shadow-lg transition-shadow">
            <SupplierIntegration inventory={inventory} />
          </Link>
          <Link
            to="/analytics"
            className="bg-white shadow-md rounded-lg p-4 hover:shadow-lg transition-shadow col-span-full"
          >
            <Analytics inventory={inventory} />
          </Link>
        </div>
      </div>
    </div>
  )
}

export default HomePage
