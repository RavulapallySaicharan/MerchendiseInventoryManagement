"use client"

import type React from "react"
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Package, User, Lock } from "lucide-react"

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    if (username === "admin" && password === "admin") {
      navigate("/home")
    } else {
      alert("Invalid credentials. Please try again.")
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-400 to-purple-500 flex justify-center items-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <div className="flex justify-center mb-6">
          <Package className="w-16 h-16 text-blue-500" />
        </div>
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Login to Dashboard</h2>
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
              Username
            </label>
            <div className="flex items-center border rounded-md">
              <User className="w-5 h-5 text-gray-400 mx-3" />
              <input
                className="appearance-none border-none w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none"
                id="username"
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <div className="flex items-center border rounded-md">
              <Lock className="w-5 h-5 text-gray-400 mx-3" />
              <input
                className="appearance-none border-none w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none"
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
          <div className="flex items-center justify-center">
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
              type="submit"
            >
              Sign In
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default LoginPage

