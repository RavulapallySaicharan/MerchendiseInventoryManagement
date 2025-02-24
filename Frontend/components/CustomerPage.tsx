import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const CustomerPage: React.FC = () => {
    const [products, setProducts] = useState([]);
    const [reviews, setReviews] = useState<{ [key: number]: string }>({});
    const [ratings, setRatings] = useState<{ [key: number]: number }>({});
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

    return (
        <div className="container mx-auto p-6 bg-gray-100 min-h-screen">
            <nav className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white p-4 flex justify-between items-center shadow-lg rounded-lg">
                <h1 className="text-3xl font-bold">Customer Portal</h1>
                <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg shadow-md">Logout</button>
            </nav>
            <h1 className="text-3xl font-bold mt-6 text-center text-gray-800">Our Products</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                {products.map(product => (
                    <div key={product.id} className="bg-white shadow-md rounded-lg p-6 transition-transform transform hover:scale-105">
                        <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover rounded-lg mb-4" />
                        <h2 className="text-2xl font-semibold text-gray-800">{product.name}</h2>
                        <p className="text-gray-600 mt-2">{product.description}</p>
                        <p className="font-bold text-lg text-blue-700 mt-2">Price: ${product.price}</p>
                        <Link to={`/purchase/${product.id}`} className="block text-center bg-blue-600 text-white px-4 py-2 rounded-lg mt-4 shadow-md hover:bg-blue-700 transition-all">Purchase</Link>
                        <div className="mt-4 border-t pt-4">
                            <h3 className="text-lg font-semibold text-gray-800">Write a Review</h3>
                            <div className="mt-2 flex flex-col gap-2">
                                <textarea 
                                    className="w-full border rounded-lg p-2 shadow-sm focus:ring focus:ring-blue-300" 
                                    placeholder="Write your review here..." 
                                    value={reviews[product.id] || ""} 
                                    onChange={(e) => setReviews({ ...reviews, [product.id]: e.target.value })}
                                />
                                <div className="flex items-center gap-2">
                                    <label className="font-semibold">Rating:</label>
                                    <select 
                                        className="border rounded-lg p-2 shadow-sm focus:ring focus:ring-blue-300" 
                                        value={ratings[product.id] || 1} 
                                        onChange={(e) => setRatings({ ...ratings, [product.id]: Number(e.target.value) })}
                                    >
                                        {[1, 2, 3, 4, 5].map(num => (
                                            <option key={num} value={num}>{num} Star{num > 1 ? "s" : ""}</option>
                                        ))}
                                    </select>
                                </div>
                                <button onClick={() => handleReviewSubmit(product.id)} className="bg-green-500 text-white px-4 py-2 rounded-lg mt-2 w-full shadow-md hover:bg-green-600 transition-all">Submit Review</button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CustomerPage;
