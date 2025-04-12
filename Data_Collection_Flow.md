# SpaceX Data Collection Flow

```mermaid
graph TD
    A[Start Data Collection] --> B[SpaceX REST API]
    B --> C[Launch Data]
    B --> D[Payload Data]
    B --> E[Core Data]
    
    C --> F[Launch Site]
    C --> G[Launch Date]
    C --> H[Launch Success]
    
    D --> I[Payload Mass]
    D --> J[Payload Type]
    D --> K[Orbit Type]
    
    E --> L[Core Reuse Count]
    E --> M[Landing Success]
    E --> N[Landing Type]
    
    F --> O[Data Processing]
    G --> O
    H --> O
    I --> O
    J --> O
    K --> O
    L --> O
    M --> O
    N --> O
    
    O --> P[Feature Engineering]
    P --> Q[Final Dataset]
```

## Key API Endpoints Used

1. **Launches API**
   - `GET /v4/launches`
   - `GET /v4/launches/{id}`
   - Key fields: launch_site, launch_date_utc, success

2. **Payloads API**
   - `GET /v4/payloads`
   - `GET /v4/payloads/{id}`
   - Key fields: mass_kg, type, orbit

3. **Cores API**
   - `GET /v4/cores`
   - `GET /v4/cores/{id}`
   - Key fields: reuse_count, landing_success, landing_type

## Data Collection Process

1. **API Authentication**
   - No authentication required for public endpoints
   - Rate limiting: 30 requests per minute

2. **Data Extraction**
   - Pagination handling for large datasets
   - Error handling and retry logic
   - Data validation and cleaning

3. **Data Transformation**
   - JSON to structured format
   - Date/time standardization
   - Missing value handling
   - Feature extraction

4. **Data Storage**
   - Structured storage in pandas DataFrame
   - CSV export for persistence
   - Version control for dataset changes 