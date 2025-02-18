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

// Updated mock data with more products and image URLs
const initialInventory = [
  {
    id: 1,
    name: "Branded T-shirt",
    quantity: 100,
    lowStockThreshold: 20,
    batchInfo: "Batch A",
    supplier: "Supplier X",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 2,
    name: "Mug",
    quantity: 50,
    lowStockThreshold: 10,
    batchInfo: "Batch B",
    supplier: "Supplier Y",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 3,
    name: "Keychain",
    quantity: 200,
    lowStockThreshold: 30,
    batchInfo: "Batch C",
    supplier: "Supplier Z",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 4,
    name: "Reusable Ice Cream Container",
    quantity: 75,
    lowStockThreshold: 15,
    batchInfo: "Batch D",
    supplier: "Supplier W",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 5,
    name: "Branded Cap",
    quantity: 80,
    lowStockThreshold: 15,
    batchInfo: "Batch E",
    supplier: "Supplier X",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 6,
    name: "Notebook",
    quantity: 120,
    lowStockThreshold: 25,
    batchInfo: "Batch F",
    supplier: "Supplier Y",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 7,
    name: "Water Bottle",
    quantity: 90,
    lowStockThreshold: 20,
    batchInfo: "Batch G",
    supplier: "Supplier Z",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 8,
    name: "Tote Bag",
    quantity: 60,
    lowStockThreshold: 12,
    batchInfo: "Batch H",
    supplier: "Supplier W",
    image: "/placeholder.svg?height=100&width=100",
  },
]

const HomePage: React.FC = () => {
  const [inventory, setInventory] = useState(initialInventory)
  const navigate = useNavigate()

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setInventory((prevInventory) =>
        prevInventory.map((item) => ({
          ...item,
          quantity: Math.max(0, item.quantity + Math.floor(Math.random() * 5) - 2),
        })),
      )
    }, 5000)

    return () => clearInterval(interval)
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

