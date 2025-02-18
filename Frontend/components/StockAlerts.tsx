import type React from "react"
import { AlertTriangle } from "lucide-react"

interface InventoryItemType {
  id: number
  name: string
  quantity: number
  lowStockThreshold: number
}

interface StockAlertsProps {
  inventory: InventoryItemType[]
}

const StockAlerts: React.FC<StockAlertsProps> = ({ inventory }) => {
  const lowStockItems = inventory.filter((item) => item.quantity <= item.lowStockThreshold)

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <div className="flex items-center mb-4">
        <AlertTriangle className="w-6 h-6 text-yellow-500 mr-2" />
        <h2 className="text-xl font-semibold">Stock Alerts</h2>
      </div>
      {lowStockItems.length === 0 ? (
        <p className="text-green-600">No low stock alerts</p>
      ) : (
        <ul className="space-y-2">
          {lowStockItems.map((item) => (
            <li key={item.id} className="bg-red-100 p-2 rounded">
              <span className="font-semibold">{item.name}</span> - Current stock: {item.quantity} (Low stock threshold:{" "}
              {item.lowStockThreshold})
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default StockAlerts

