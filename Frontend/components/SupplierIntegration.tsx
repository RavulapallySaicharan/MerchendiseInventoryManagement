import type React from "react"
import { Truck } from "lucide-react"

interface InventoryItemType {
  id: number
  name: string
  quantity: number
  lowStockThreshold: number
  supplier: string
}

interface SupplierIntegrationProps {
  inventory: InventoryItemType[]
}

const SupplierIntegration: React.FC<SupplierIntegrationProps> = ({ inventory }) => {
  const itemsToReorder = inventory.filter((item) => item.quantity <= item.lowStockThreshold)

  return (
    <div className="bg-white rounded-lg p-4">
      <div className="flex items-center mb-4">
        <Truck className="w-6 h-6 text-green-500 mr-2" />
        <h2 className="text-xl font-semibold">Supplier Integration</h2>
      </div>
      <p>{itemsToReorder.length} items need reordering</p>
    </div>
  )
}

export default SupplierIntegration

