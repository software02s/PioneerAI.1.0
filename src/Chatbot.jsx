import { useState, useEffect, useRef } from 'react';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [rating, setRating] = useState(null);
    const [showRating, setShowRating] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        fetchMessages();
    }, []);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }

        if (messages.length > 0) {
            const lastMessage = messages[messages.length - 1];
            if (lastMessage.sender === 'user' && /bye|goodbye|see you|exit/i.test(lastMessage.text)) {
                setShowRating(true);
            }
        }
    }, [messages]);

    const fetchMessages = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/messages');
            const data = await response.json();
            setMessages(data);
        } catch (error) {
            console.error("Error fetching messages:", error);
        }
    };

    const handleSendMessage = async (e) => {
        if (e) e.preventDefault();

        if (input.trim()) {
            const newMessage = { text: input, sender: 'user', time: new Date() };
            setMessages((prevMessages) => [...prevMessages, newMessage]);
            setInput('');
            setLoading(true);

            try {
                const response = await fetch('http://localhost:5000/api/message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: input }),
                });

                const data = await response.json();
                const botMessage = {
                    text: data.response,
                    sender: 'bot',
                    time: new Date(),
                };

                setMessages((prevMessages) => [...prevMessages, botMessage]);
            } catch (error) {
                console.error("Error sending message:", error);
            } finally {
                setLoading(false);
            }
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            handleSendMessage(e);
        }
    };

    const formatTime = (time) => {
        return time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    const handleRatingSubmit = async () => {
        if (rating !== null) {
            try {
                await fetch('http://localhost:5000/api/rating', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ rating }),
                });
                setShowModal(true);
                setRating(null);
                setShowRating(false);
            } catch (error) {
                console.error("Error submitting rating:", error);
            }
        } else {
            alert("Please give a rating before submitting.");
        }
    };

    const renderStars = () => {
        const stars = [];
        for (let i = 1; i <= 5; i++) {
            stars.push(
                <span
                    key={i}
                    className={`cursor-pointer text-3xl transition-all duration-300 ${rating >= i ? 'text-yellow-400' : 'text-gray-500'}`}
                    onClick={() => setRating(i)}
                >
                    ★
                </span>
            );
        }
        return stars;
    };

    const FeedbackModal = () => {
        return (
            <div className={`fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 ${showModal ? 'block' : 'hidden'}`}>
                <div className="bg-white p-8 rounded-lg text-center shadow-lg max-w-sm w-full">
                    <h3 className="text-2xl font-semibold mb-4 text-gray-800">Thank You for Your Feedback!</h3>
                    <p className="mb-4 text-gray-600">We appreciate your response. Your feedback helps us improve.</p>
                    <button
                        onClick={() => setShowModal(false)}
                        className="px-6 py-2 bg-gray-800 text-white rounded-full transition duration-300 hover:bg-gray-700"
                    >
                        Close
                    </button>
                </div>
            </div>
        );
    };

    return (
        <div
            className="absolute bottom-8 right-8 w-full max-w-lg p-6 rounded-xl flex flex-col space-y-6 overflow-hidden border-2 border-gray-300 z-50 shadow-lg"
            style={{
                backgroundImage: 'url(/last.jpg)', // Path to your background image
                backgroundSize: 'cover', // Ensure it covers the full div
                backgroundPosition: 'center', // Keep it centered
            }}
        >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-300">
                <div className="flex items-center space-x-2">
                    <img
                        src="/avatarBot.png"
                        alt="bot-avatar"
                        className="w-12 h-12 rounded-full transition-all duration-300 transform"
                    />
                    <div className="font-semibold text-white text-xl">PioneerAI 1.0</div>
                </div>
            </div>

            {/* Chat Messages */}
            <div className="flex flex-col space-y-4 overflow-y-auto flex-grow p-4" style={{ minHeight: '400px', maxHeight: '500px' }}>
                {messages.map((message, index) => (
                    <div key={index} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div
                            className={`flex items-center space-x-2 max-w-[75%] p-4 rounded-xl break-words transition-all duration-300 ease-in-out ${message.sender === 'user' ? 'bg-black text-white rounded-tl-lg rounded-br-lg shadow-md' : 'bg-gray-100 text-gray-800 rounded-tr-lg rounded-bl-lg shadow-sm'}`}
                        >
                            {message.sender === 'bot' && (
                                <img src="/avatarBot.png" alt="bot-avatar" className="w-10 h-10 rounded-full" />
                            )}
                            <span>{message.text}</span>
                        </div>
                        <span className="text-xs text-gray-500 mt-1 ml-2">{formatTime(new Date(message.time))}</span>
                    </div>
                ))}

                {loading && (
                    <div className="self-start p-4 bg-gray-200 text-gray-500 rounded-lg animate-pulse">
                        <i className="text-gray-400">Bot is typing...</i>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Field */}
            <div className="flex items-center space-x-4 border-t pt-4 mt-4">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyPress}
                    className="flex-1 p-4 border border-gray-300 rounded-full bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-600 placeholder-gray-400"
                    placeholder="Type a message..."
                />
                <button
                    onClick={(e) => handleSendMessage(e)}
                    className="p-4 bg-blue-600 hover:bg-blue-700 text-white rounded-full transition duration-300"
                >
                    <i className="fas fa-paper-plane"></i>
                </button>
            </div>

            {/* Rating Section */}
            {showRating && (
                <div className="mt-4 flex flex-col items-center">
                    <div className="text-white">How was your experience?</div>
                    <div className="flex space-x-2 mt-2">
                        {renderStars()}
                    </div>
                    <button
                        onClick={handleRatingSubmit}
                        className="mt-4 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-full"
                    >
                        Submit Rating
                    </button>
                </div>
            )}

            {/* Feedback Modal */}
            <FeedbackModal />
        </div>
    );
};

export default Chatbot;
