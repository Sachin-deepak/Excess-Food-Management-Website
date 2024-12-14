# Excess Food Management Website (Foodsaver)

A transformative platform designed to tackle food wastage and food insecurity by connecting donors with surplus food to those in need, leveraging mobile technology for sustainable and equitable solutions.

## Table of Contents
- [Abstract](#abstract)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Future Scope](#future-scope)

## Abstract
India wastes nearly 40% of its food annually, while millions face food insecurity. Foodsaver bridges this gap by creating a platform where individuals and organizations can donate excess food or sell groceries at discounted prices. NGOs act as intermediaries, redistributing food to low-income families. The app uses real-time alerts and user-friendly forums for donations, aiming to reduce food waste by 25% annually.

## Features
1. **User Management**:
   - Role-based sign-up (Donor/Receiver).
   - Profile customization.
2. **Donor Dashboard**:
   - Post food donations with details.
   - Auto-remove expired donations.
3. **Receiver Dashboard**:
   - Browse available donations.
   - Interact with donors.
4. **Forum**:
   - Community-driven discussions.
5. **Food Requests**:
   - Post specific requirements.
   - Collaborative discussions.
6. **Analytics**:
   - Visualize donation trends.

## Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MongoDB
- **Libraries**:
  - `streamlit` (UI)
  - `pymongo` (Database)
  - `bcrypt` (Security)
  - `datetime` (Time management)
  - `pandas` (Analytics)

## Architecture
The platform connects donors with receivers through a modular system:
- **Modules**:
  - User Management
  - Donation Management
  - Messaging System
  - Analytics and Reporting

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Foodsaver.git
   cd Foodsaver
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage
- **Donors**: Post available food for donation.
- **Receivers**: Browse and request donations.
- **Community**: Engage in forums for collaborative solutions.

## Contributing
Contributions are welcome! Please follow the [contribution guidelines](CONTRIBUTING.md).

## Future Scope
- Expand to additional cities.
- Introduce AI-driven demand forecasting.
- Integrate payment systems for grocery purchases.
