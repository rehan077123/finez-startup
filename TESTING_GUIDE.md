# Quick Start Guide - FineZ Decision Engine Testing

## Prerequisites

- Backend running on http://localhost:8000
- Frontend running on http://localhost:3000
- MongoDB Atlas connected

## Step-by-Step Testing

### Step 1: Verify Backend Endpoints

```bash
# Navigate to backend
cd backend

# Install requests if needed
pip install requests

# Run the API test suite
python test_decision_engine.py
```

**Expected Output**:
```
============================================================
FineZ Decision Engine API Test Suite
============================================================

Testing: GET /stacks/outcomes
✓ Status 200
Response keys: stacks
  → Found 6 stacks

Testing: GET /stacks/outcomes/dropshipping-2026
✓ Status 200
Response keys: stack, products, workflow_steps
  → Found N products

... (tests for all 6 stacks)

Testing: POST /stacks/track-engagement
✓ Status 200
Response keys: acknowledged

Testing: GET /admin/stacks/analytics
✓ Status 200
Response keys: stacks
  → Found X aggregated stacks

============================================================
Test Suite Complete!
============================================================
```

### Step 2: Seed Trust Metadata (Optional)

If you want to add trust confidence fields to existing products:

```bash
cd backend
python seed_trust_metadata.py
```

**Expected Output**:
```
Found 45 products to update
✓ Updated: Winning Dropshipper → {'difficulty': 'intermediate', 'roi': 'high', ...}
✓ Updated: Claude 3 Opus → {'difficulty': 'beginner', 'roi': 'high', ...}
...
✅ Successfully updated 35 products with trust metadata!
```

### Step 3: Test Frontend Navigation

1. **Visit Homepage**
   - Go to http://localhost:3000
   - Should see 6 outcome stack cards with:
     - Emoji icon
     - Stack title
     - Description
     - Setup time, difficulty, ROI, earning potential
     - "Explore Stack" button

2. **Click "Explore Stack" button**
   - Should navigate to `/stacks/{stackId}`
   - URL example: http://localhost:3000/stacks/dropshipping-2026

3. **On Stack Detail Page**
   - Should see hero banner with gradient
   - Quick stats at top (ROI, setup time, difficulty)
   - "Getting Started" section with 4 numbered steps
   - Social proof box
   - "Everything You Need" section with product grid
   - Products should show trust metadata badges
   - "Start Your Journey" CTA button

### Step 4: Verify Engagement Tracking

1. **View Stack Page**
   - Should automatically track "view" engagement

2. **Open Browser Console** (F12)
   - Should see logged message: "Engagement tracked"

3. **Check MongoDB** (Optional)
   ```bash
   # In MongoDB Compass or CLI
   db.stack_engagements.find().sort({_id: -1}).limit(5)
   
   # Should see recent engagement records:
   {
     "_id": ObjectId(...),
     "stack_id": "dropshipping-2026",
     "action": "view",
     "timestamp": ISODate("2024-..."),
   }
   ```

### Step 5: Test All 6 Stacks

Click through each stack to verify:

1. **Dropshipping 2026** (Pink/Orange gradient)
   - URL: /stacks/dropshipping-2026
   - Should load and display products

2. **AI Creator Stack** (Blue/Cyan gradient)
   - URL: /stacks/ai-creator-stack
   - Should load and display products

3. **Affiliate Mastery** (Green gradient)
   - URL: /stacks/affiliate-mastery
   - Should load and display products

4. **YouTube Automation** (Red gradient)
   - URL: /stacks/youtube-automation
   - Should load and display products

5. **Budget Office Setup** (Purple gradient)
   - URL: /stacks/budget-office-setup
   - Should load and display products

6. **Gym Transformation** (Orange gradient)
   - URL: /stacks/gym-transformation
   - Should load and display products

### Step 6: Check ProductCard Trust Badges

On any stack detail page:
1. Scroll to "Everything You Need" section
2. Look for products with trust metadata showing:
   - "Difficulty: Intermediate" (emerald-400)
   - "ROI: High" (color-coded)
   - "Setup Time: 1-2 hours" (white)
   - "Earning: ₹5k-20k" (amber-400)

### Step 7: Test Admin Analytics Endpoint

```bash
# Get analytics data
curl http://localhost:8000/admin/stacks/analytics

# Should return:
{
  "stacks": [
    {
      "id": "dropshipping-2026",
      "title": "Dropshipping 2026",
      "views": 1,
      "explores": 0,
      "add_to_cart": 0,
      "purchases": 0,
      "conversion_rate": 0.0,
      "estimated_revenue": "₹0"
    },
    ...
  ],
  "total_views": X,
  "total_engagements": Y,
  "timestamp": "2024-..."
}
```

## Troubleshooting

### Problem: "Cannot GET /stacks/dropshipping-2026"

**Solution**: Make sure the route is added to App.js:
```javascript
<Route path="/stacks/:stackId" element={<OutcomeStackPage />} />
```

### Problem: Products not showing on stack page

**Solution**: 
1. Check browser console for errors
2. Verify backend is running:
   ```bash
   curl http://localhost:8000/stacks/outcomes/dropshipping-2026
   ```
3. Ensure products have correct category mapping

### Problem: trust metadata not displaying on ProductCard

**Solution**:
1. Seed trust metadata:
   ```bash
   python backend/seed_trust_metadata.py
   ```
2. Verify products in MongoDB have the fields:
   ```bash
   db.products.findOne({}, {difficulty: 1, roi: 1, setupTime: 1})
   ```

### Problem: Engagement tracking not working

**Solution**:
1. Check backend for errors:
   ```bash
   # Tail backend logs
   ```
2. Verify MongoDB connection by checking admin/stacks/analytics endpoint
3. Check browser network tab for POST requests

## Performance Testing

### Load Time Expectations

- Homepage load: < 2 seconds
- Stack detail page: < 1.5 seconds (with products)
- Product grid render: < 0.5 seconds
- Engagement tracking: < 100ms (async)

### Database Queries

```javascript
// Stack with products (should be < 500ms)
db.products.find({category: {$in: [...]}}).limit(12)

// Engagement aggregation (should be < 1000ms)
db.stack_engagements.aggregate([
  {$match: {timestamp: {$gte: ISODate("...")}}},
  {$group: {_id: "$stack_id", count: {$sum: 1}}}
])
```

## Next Steps

After verification:

1. **Data Seeding** - Run seed_trust_metadata.py to populate products
2. **A/B Testing** - Monitor which stacks convert best
3. **Optimization** - Adjust product order based on engagement
4. **Enhancement** - Add AI semantic search to map queries → stacks
5. **Scaling** - Cache stack data, implement pagination

## Testing Checklist

- [ ] All 6 stacks load successfully
- [ ] Navigation from home → stack works
- [ ] Trust metadata badges display on products
- [ ] Engagement tracking sends POST requests
- [ ] Admin analytics endpoint returns data
- [ ] No console errors
- [ ] Mobile responsive design works
- [ ] Load times under targets
- [ ] MongoDB queries performant

## API Test Examples

### Get All Stacks
```bash
curl -X GET http://localhost:8000/stacks/outcomes
```

### Get Specific Stack
```bash
curl -X GET http://localhost:8000/stacks/outcomes/dropshipping-2026
```

### Track Engagement
```bash
curl -X POST http://localhost:8000/stacks/track-engagement \
  -H "Content-Type: application/json" \
  -d '{"stack_id":"dropshipping-2026","action":"view"}'
```

### Get Analytics
```bash
curl -X GET http://localhost:8000/admin/stacks/analytics
```

## Logs to Monitor

### Backend
- Stack query execution time
- Product filtering performance
- Engagement document creation

### Frontend
- Navigation events
- Component render times
- API response times

### Database
- Query performance
- Index usage
- Collection sizes

---

**Happy Testing!** 🚀

For issues, check the console (Ctrl+Shift+K) and ensure all servers are running.
