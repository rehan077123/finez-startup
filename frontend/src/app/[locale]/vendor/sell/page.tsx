'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Upload, AlertCircle, CheckCircle } from 'lucide-react';

export default function SellProductPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [selectedProductType, setSelectedProductType] = useState<'affiliate' | 'dropship' | null>(null);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    originalPrice: '',
    category: 'Electronics',
    affiliateLink: '',
    affiliateNetwork: 'Amazon Associates',
    productType: 'affiliate',
    image: '',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    // If Affiliate Network changes to "Other", show modal
    if (name === 'affiliateNetwork' && value === 'Other') {
      setShowTypeModal(true);
      return;
    }

    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectProductType = (type: 'affiliate' | 'dropship') => {
    setSelectedProductType(type);
    setFormData(prev => ({ 
      ...prev, 
      affiliateNetwork: type === 'affiliate' ? 'Other Affiliate' : 'Dropship',
      productType: type
    }));
    setShowTypeModal(false);
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      // Validate required fields
      if (!formData.title || !formData.description || !formData.price || !formData.affiliateLink) {
        setError('Please fill in all required fields');
        setLoading(false);
        return;
      }

      // Validate affiliate link
      if (!formData.affiliateLink.startsWith('http')) {
        setError('Please enter a valid affiliate link starting with http:// or https://');
        setLoading(false);
        return;
      }

      // Create FormData for multipart upload
      const uploadData = new FormData();
      uploadData.append('title', formData.title);
      uploadData.append('description', formData.description);
      uploadData.append('price', formData.price);
      uploadData.append('originalPrice', formData.originalPrice || formData.price);
      uploadData.append('category', formData.category);
      uploadData.append('affiliateLink', formData.affiliateLink);
      uploadData.append('affiliateNetwork', formData.affiliateNetwork);
      uploadData.append('type', selectedProductType === 'dropship' ? 'dropship' : 'affiliate');
      uploadData.append('verified', 'false');

      if (imageFile) {
        uploadData.append('image', imageFile);
      }

      const response = await fetch('http://localhost:8000/api/vendor/products/upload', {
        method: 'POST',
        body: uploadData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to upload product');
      }

      const result = await response.json();
      
      setSuccess(`Product uploaded successfully as ${selectedProductType}! It will appear on the marketplace once verified.`);
      setFormData({
        title: '',
        description: '',
        price: '',
        originalPrice: '',
        category: 'Electronics',
        affiliateLink: '',
        affiliateNetwork: 'Amazon Associates',
        productType: 'affiliate',
        image: '',
      });
      setImageFile(null);
      setImagePreview(null);
      setSelectedProductType(null);

      // Redirect after 2 seconds
      setTimeout(() => {
        router.push(selectedProductType === 'dropship' ? '/dropship' : '/affiliate');
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">Sell Your Products</h1>
          <p className="text-slate-600">Upload your affiliate and dropship products to earn commissions</p>
        </div>

        {/* Alert Messages */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
            <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-red-900">Error</h3>
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-start gap-3">
            <CheckCircle className="text-green-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-green-900">Success!</h3>
              <p className="text-green-700">{success}</p>
            </div>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8">
          
          {/* Image Upload */}
          <div className="mb-8">
            <label className="block text-sm font-semibold text-slate-900 mb-3">
              Product Image * 
            </label>
            <div className="relative border-2 border-dashed border-slate-300 rounded-lg p-8 text-center hover:border-blue-400 transition">
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              {imagePreview ? (
                <div className="space-y-3">
                  <img src={imagePreview} alt="Preview" className="h-40 mx-auto object-contain rounded" />
                  <p className="text-sm text-slate-600">Click to change image</p>
                </div>
              ) : (
                <div className="space-y-2">
                  <Upload className="h-12 w-12 text-slate-400 mx-auto" />
                  <p className="text-slate-600">Click or drag to upload image</p>
                  <p className="text-xs text-slate-500">PNG, JPG, WebP up to 10MB</p>
                </div>
              )}
            </div>
          </div>

          {/* Product Title */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-900 mb-2">
              Product Title *
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              placeholder="e.g., Samsung Galaxy S24 Ultra"
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              maxLength={200}
            />
          </div>

          {/* Description */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-900 mb-2">
              Product Description *
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="Describe your product features, benefits, and specifications..."
              rows={5}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              maxLength={2000}
            />
          </div>

          {/* Price Fields */}
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-semibold text-slate-900 mb-2">
                Current Price (₹) *
              </label>
              <input
                type="number"
                name="price"
                value={formData.price}
                onChange={handleInputChange}
                placeholder="e.g., 44249"
                step="0.01"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-900 mb-2">
                Original Price (₹)
              </label>
              <input
                type="number"
                name="originalPrice"
                value={formData.originalPrice}
                onChange={handleInputChange}
                placeholder="e.g., 74999"
                step="0.01"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Category */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-900 mb-2">
              Category *
            </label>
            <select
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Electronics">Electronics</option>
              <option value="Fashion">Fashion</option>
              <option value="Home & Kitchen">Home & Kitchen</option>
              <option value="Sports">Sports</option>
              <option value="Books">Books</option>
              <option value="Toys">Toys</option>
              <option value="Health & Beauty">Health & Beauty</option>
              <option value="Gadgets">Gadgets</option>
              <option value="Accessories">Accessories</option>
              <option value="Other">Other</option>
            </select>
          </div>

          {/* Affiliate Network */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-900 mb-2">
              Affiliate Network *
            </label>
            <select
              name="affiliateNetwork"
              value={formData.affiliateNetwork}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Amazon Associates">Amazon Associates</option>
              <option value="Flipkart Affiliate">Flipkart Affiliate</option>
              <option value="CueLinks">CueLinks</option>
              <option value="Other">Other - Will Ask for Type</option>
            </select>
          </div>

          {/* Product Type Display */}
          {selectedProductType && (
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-900">
                <strong>Product Type:</strong> {selectedProductType.charAt(0).toUpperCase() + selectedProductType.slice(1)}
              </p>
            </div>
          )}

          {/* Affiliate Link */}
          <div className="mb-8">
            <label className="block text-sm font-semibold text-slate-900 mb-2">
              Affiliate Link *
            </label>
            <input
              type="url"
              name="affiliateLink"
              value={formData.affiliateLink}
              onChange={handleInputChange}
              placeholder="https://www.amazon.in/dp/ASIN?tag=yourtag or your dropship link"
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-xs text-slate-500 mt-2">Must be a valid affiliate or dropship link with your tracking ID</p>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white font-bold py-3 rounded-lg transition"
          >
            {loading ? 'Uploading...' : 'Upload Product'}
          </button>

          {/* Info Box */}
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>Note:</strong> All products will be reviewed by our team before appearing on the marketplace. This ensures quality and authenticity for our users.
            </p>
          </div>
        </form>
      </div>

      {/* Modal for Type Selection */}
      {showTypeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
          <div className="bg-white rounded-lg shadow-2xl max-w-md w-full p-8">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">What type of product are you selling?</h2>
            <p className="text-slate-600 mb-6">Choose whether this is an affiliate product or a dropship product</p>

            <div className="space-y-3">
              <button
                onClick={() => handleSelectProductType('affiliate')}
                className="w-full p-4 border-2 border-blue-200 hover:border-blue-600 hover:bg-blue-50 rounded-lg transition text-left"
              >
                <h3 className="font-bold text-slate-900">🔗 Affiliate Product</h3>
                <p className="text-sm text-slate-600">Commission-based products from affiliate networks</p>
              </button>

              <button
                onClick={() => handleSelectProductType('dropship')}
                className="w-full p-4 border-2 border-purple-200 hover:border-purple-600 hover:bg-purple-50 rounded-lg transition text-left"
              >
                <h3 className="font-bold text-slate-900">📦 Dropship Product</h3>
                <p className="text-sm text-slate-600">Inventory-based products from dropship suppliers</p>
              </button>
            </div>

            <button
              onClick={() => setShowTypeModal(false)}
              className="w-full mt-4 p-2 text-slate-600 hover:text-slate-900"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
