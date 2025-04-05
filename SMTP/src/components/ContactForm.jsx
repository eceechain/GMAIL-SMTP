import { useState } from 'react';
import { motion } from 'framer-motion';
import { Mail, Send, User, LoaderCircle } from 'lucide-react';

export default function ContactForm() {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus(null);

    try {
      const res = await fetch('http://localhost:5000/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await res.json();
      setLoading(false);

      if (res.ok) {
        setStatus({ type: 'success', message: data.message });
        setFormData({ name: '', email: '', message: '' });
      } else {
        setStatus({ type: 'error', message: data.message || 'Failed to send message' });
      }
    } catch (err) {
      setLoading(false);
      setStatus({ type: 'error', message: 'Server error. Please try again.' });
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="w-full max-w-3xl mx-auto mt-20 bg-white p-12 rounded-3xl shadow-2xl"
    >
      <motion.h2
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-4xl font-extrabold text-center text-blue-600 mb-10 flex items-center justify-center gap-3"
      >
        <Mail className="w-7 h-7" />
        Contact Us
      </motion.h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {['name', 'email'].map((field, i) => (
          <motion.div
            key={field}
            initial={{ x: -30, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.1 * i }}
            className="relative"
          >
            {field === 'name' ? (
              <User className="absolute left-4 top-3.5 text-gray-400" />
            ) : (
              <Mail className="absolute left-4 top-3.5 text-gray-400" />
            )}
            <input
              type={field === 'email' ? 'email' : 'text'}
              name={field}
              placeholder={`Your ${field.charAt(0).toUpperCase() + field.slice(1)}`}
              value={formData[field]}
              onChange={handleChange}
              required
              className="w-full pl-12 text-lg border border-gray-300 p-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </motion.div>
        ))}

        <motion.div
          initial={{ x: 30, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.25 }}
        >
          <textarea
            name="message"
            placeholder="Your Message"
            value={formData.message}
            onChange={handleChange}
            required
            className="w-full text-lg border border-gray-300 p-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
            rows="6"
          ></textarea>
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.98 }}
          className="flex justify-center"
        >
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-10 py-4 text-lg font-semibold rounded-xl flex items-center gap-2 hover:bg-blue-700 transition"
          >
            {loading ? <LoaderCircle className="animate-spin w-5 h-5" /> : <Send />}
            {loading ? 'Sending...' : 'Send Message'}
          </button>
        </motion.div>

        {status && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className={`text-center mt-6 text-lg font-medium ${
              status.type === 'success' ? 'text-green-600' : 'text-red-500'
            }`}
          >
            {status.message}
          </motion.p>
        )}
      </form>
    </motion.div>
  );
}
