import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, X, Star } from 'lucide-react';

const CustomerPage: React.FC = () => {
    const [products, setProducts] = useState([]);
    const [cart, setCart] = useState<{ [key: number]: { product: any, quantity: number } }>({});
    const [reviews, setReviews] = useState<{ [key: number]: string }>({});
    const [ratings, setRatings] = useState<{ [key: number]: number }>({});
    const [showCart, setShowCart] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await fetch('http://localhost:8000/products');
                const data = await response.json();
                setProducts(data);
            } catch (error) {
                console.error('Error fetching products:', error);
            }
        };
        fetchProducts();
    }, []);

    const handleLogout = () => {
        navigate("/");
    };

    const handleAddToCart = (product) => {
        setCart(prevCart => {
            const updatedCart = { ...prevCart };
            if (updatedCart[product.id]) {
                updatedCart[product.id].quantity += 1;
            } else {
                updatedCart[product.id] = { product, quantity: 1 };
            }
            return updatedCart;
        });
    };

    const handleReviewSubmit = async (productId: number) => {
        try {
            const response = await fetch("http://localhost:8000/reviews/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                },
                body: JSON.stringify({
                    product_id: productId,
                    rating: ratings[productId] || 1,
                    review_text: reviews[productId] || ""
                })
            });

            if (!response.ok) {
                throw new Error("Failed to submit review");
            }

            alert("Review submitted successfully!");
            setReviews(prev => ({ ...prev, [productId]: "" }));
            setRatings(prev => ({ ...prev, [productId]: 1 }));
        } catch (error) {
            console.error("Error submitting review:", error);
            alert("Failed to submit review");
        }
    };

    const handleCheckout = async () => {
        try {
            const purchases = Object.values(cart).map(({ product, quantity }) => ({
                product_id: product.id,
                quantity
            }));

            const response = await fetch("http://localhost:8000/purchase", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                },
                body: JSON.stringify(purchases)
            });

            if (!response.ok) {
                throw new Error("Purchase failed");
            }

            alert("Purchase successful!");
            setCart({});
            setShowCart(false);
        } catch (error) {
            console.error("Error during checkout:", error);
            alert("Purchase failed");
        }
    };

    return (
        <div className="container mx-auto p-6 bg-gray-100 min-h-screen">
            <nav className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white p-4 flex justify-between items-center shadow-lg rounded-lg">
                <h1 className="text-3xl font-bold">Customer Portal</h1>
                <div className="flex items-center gap-4">
                    <button onClick={() => setShowCart(true)} className="relative">
                        <ShoppingCart className="w-8 h-8 text-white" />
                        {Object.keys(cart).length > 0 && (
                            <span className="absolute -top-1 -right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">{Object.keys(cart).length}</span>
                        )}
                    </button>
                    <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg shadow-md">Logout</button>
                </div>
            </nav>
            
            <h1 className="text-3xl font-bold mt-6 text-center text-gray-800">Our Products</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                {products.map(product => (
                    <div key={product.id} className="bg-white shadow-md rounded-lg p-6 transition-transform transform hover:scale-105">
                        <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover rounded-lg mb-4" />
                        <h2 className="text-2xl font-semibold text-gray-800">{product.name}</h2>
                        <p className="text-gray-600 mt-2">{product.description}</p>
                        <p className="font-bold text-lg text-blue-700 mt-2">Price: ${product.price}</p>
                        <button onClick={() => handleAddToCart(product)} className="block text-center bg-green-500 text-white px-4 py-2 rounded-lg mt-4 shadow-md hover:bg-green-600 transition-all w-full">Add to Cart</button>
                        <div className="mt-4">
                            <h3 className="font-bold text-lg">Leave a Review</h3>
                            <div className="flex gap-2 items-center mt-2">
                                <input type="number" min="1" max="5" value={ratings[product.id] || 1} onChange={(e) => setRatings(prev => ({ ...prev, [product.id]: parseInt(e.target.value) }))} className="border p-1 w-16 text-center" />
                                <Star className="text-yellow-500" />
                            </div>
                            <textarea value={reviews[product.id] || ""} onChange={(e) => setReviews(prev => ({ ...prev, [product.id]: e.target.value }))} className="w-full border p-2 mt-2" placeholder="Write your review..." />
                            <button onClick={() => handleReviewSubmit(product.id)} className="bg-blue-500 text-white px-4 py-2 rounded-lg mt-2 shadow-md hover:bg-blue-600 transition-all w-full">Submit Review</button>
                        </div>
                    </div>
                ))}
            </div>
            
            {showCart && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
                    <div className="bg-white p-6 rounded-lg shadow-lg w-96">
                        <h2 className="text-xl font-bold">Your Cart</h2>
                        {Object.keys(cart).length > 0 ? (
                            <ul>
                                {Object.values(cart).map(({ product, quantity }) => (
                                    <li key={product.id} className="border-b py-2">{product.name} - ${product.price} x {quantity}</li>
                                ))}
                            </ul>
                        ) : <p>Your cart is empty.</p>}
                        <button onClick={handleCheckout} className="bg-blue-500 text-white px-4 py-2 rounded-lg mt-4 w-full">Checkout</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CustomerPage;
