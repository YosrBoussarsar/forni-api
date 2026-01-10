# Frontend Integration - Product Templates

## Add to your React ManageProducts component

### 1. Add state for recommendations modal

```javascript
const [showTemplates, setShowTemplates] = useState(false);
const [recommendations, setRecommendations] = useState([]);
const [loading, setLoading] = useState(false);
```

### 2. Add function to fetch recommendations

```javascript
const fetchRecommendations = async () => {
  setLoading(true);
  try {
    const response = await fetch(
      `http://localhost:5000/product/recommendations?exclude_bakery_id=${bakeryId}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    const data = await response.json();
    setRecommendations(data.recommendations || []);
    setShowTemplates(true);
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    alert('Failed to load product templates');
  } finally {
    setLoading(false);
  }
};
```

### 3. Add function to create product from template

```javascript
const addFromTemplate = async (template) => {
  // Show a form to get bakery-specific details
  const price = prompt(`Enter your price for "${template.name}" (avg: ${template.avg_price || 'N/A'} TND):`);
  if (!price) return;
  
  const quantity = prompt(`Enter quantity available for "${template.name}":`);
  if (!quantity) return;
  
  try {
    const response = await fetch(
      `http://localhost:5000/product/from-template/${template.template_product_id}`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bakery_id: bakeryId,
          price: parseFloat(price),
          quantity_available: parseInt(quantity),
          is_available: true
        })
      }
    );
    
    if (response.ok) {
      alert(`Product "${template.name}" added successfully!`);
      setShowTemplates(false);
      // Refresh your product list
      fetchProducts();
    } else {
      const error = await response.json();
      alert(`Error: ${error.message || 'Failed to add product'}`);
    }
  } catch (error) {
    console.error('Error adding product:', error);
    alert('Failed to add product from template');
  }
};
```

### 4. Update your "Add Product" button section

```javascript
<div style={{ display: 'flex', gap: '10px' }}>
  <button 
    className="add-product-btn"
    onClick={() => setShowAddModal(true)}
  >
    + Add Custom Product
  </button>
  
  <button 
    className="browse-templates-btn"
    onClick={fetchRecommendations}
    disabled={loading}
    style={{
      background: '#2196F3',
      color: 'white',
      padding: '10px 20px',
      border: 'none',
      borderRadius: '5px',
      cursor: loading ? 'not-allowed' : 'pointer'
    }}
  >
    {loading ? 'Loading...' : '📋 Browse Templates'}
  </button>
</div>
```

### 5. Add the Templates Modal component

```javascript
{showTemplates && (
  <div className="modal-overlay" onClick={() => setShowTemplates(false)}>
    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
      <h2>Product Templates</h2>
      <p>Click "Add" to create this product for your bakery with your own pricing</p>
      
      <div className="templates-grid" style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
        gap: '20px',
        maxHeight: '500px',
        overflowY: 'auto'
      }}>
        {recommendations.map((template) => (
          <div key={template.template_product_id} className="template-card" style={{
            border: '1px solid #ddd',
            borderRadius: '8px',
            padding: '15px',
            background: 'white'
          }}>
            <h3>{template.name}</h3>
            {template.image_url && (
              <img 
                src={`http://localhost:5000${template.image_url}`} 
                alt={template.name}
                style={{ width: '100%', height: '150px', objectFit: 'cover', borderRadius: '5px' }}
              />
            )}
            <p style={{ fontSize: '0.9em', color: '#666' }}>{template.description}</p>
            
            <div style={{ marginTop: '10px' }}>
              <span className="badge">{template.category}</span>
              <span className="badge" style={{ marginLeft: '5px' }}>
                🔥 Used by {template.popularity} bakeries
              </span>
            </div>
            
            {template.avg_price && (
              <p style={{ fontSize: '0.85em', color: '#999', marginTop: '5px' }}>
                Avg price: {template.avg_price} TND
              </p>
            )}
            
            {template.allergens && (
              <p style={{ fontSize: '0.85em', color: '#e74c3c', marginTop: '5px' }}>
                ⚠️ {template.allergens}
              </p>
            )}
            
            {template.tags && (
              <p style={{ fontSize: '0.85em', color: '#3498db', marginTop: '5px' }}>
                Tags: {template.tags}
              </p>
            )}
            
            <button 
              onClick={() => addFromTemplate(template)}
              style={{
                width: '100%',
                marginTop: '10px',
                padding: '10px',
                background: '#27ae60',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer'
              }}
            >
              + Add to My Bakery
            </button>
          </div>
        ))}
      </div>
      
      {recommendations.length === 0 && (
        <p style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
          No templates available yet. Create your first product!
        </p>
      )}
      
      <button 
        onClick={() => setShowTemplates(false)}
        style={{
          marginTop: '20px',
          padding: '10px 20px',
          background: '#e74c3c',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
      >
        Close
      </button>
    </div>
  </div>
)}
```

### 6. Add CSS for modal

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  max-width: 900px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.badge {
  display: inline-block;
  background: #ecf0f1;
  padding: 3px 8px;
  border-radius: 3px;
  font-size: 0.8em;
  color: #555;
}
```

---

## Quick Test

After adding this code, you should:

1. See a new "📋 Browse Templates" button next to "Add Product"
2. Click it to see recommendations based on existing products
3. Click "Add to My Bakery" on any template
4. Enter your price and quantity
5. Product gets added to your bakery with your specific details

The backend is ready - you just need to add this frontend code! 🚀
