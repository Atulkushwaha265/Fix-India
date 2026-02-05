# NearFix - All-in-One Local Service Booking System

A comprehensive web application for booking local services similar to Uber/Zomato but for home services like plumbing, electrical work, car repair, and more.

## 🚀 Features

### User Module
- **Registration & Login**: Secure user authentication
- **Service Selection**: Choose from multiple service types
- **Location-based Requests**: Enter location and describe problems
- **Request Tracking**: Monitor service request status in real-time
- **Request History**: View all past and current service requests

### Service Provider Module
- **Helper Registration**: Service providers can register and get approved
- **Service Type Selection**: Choose specific service categories
- **Availability Management**: Set status as available/busy
- **Request Assignment**: Automatically receive nearby service requests
- **Status Updates**: Accept/reject and update request progress

### Admin Module
- **Dashboard Overview**: Complete system statistics
- **Helper Approval**: Review and approve service provider registrations
- **User Management**: View and manage all registered users
- **Service Management**: Add/remove service categories
- **Request Monitoring**: Track all service requests system-wide

### Core Features
- **Location-based Matching**: Automatic nearest helper assignment
- **Real-time Status Updates**: Track request progress
- **Multi-service Platform**: Multiple services in one system
- **Responsive Design**: Works on all devices
- **Clean UI/UX**: User-friendly interface

## 🛠 Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python with Flask
- **Database**: MySQL
- **Authentication**: Session-based with password hashing
- **Location Services**: Geolocation API integration

## 📋 Prerequisites

- Python 3.7 or higher
- MySQL Server
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd nearfix
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Create MySQL Database
```sql
CREATE DATABASE nearfix;
```

#### Import Database Schema
```bash
mysql -u root -p nearfix < database.sql
```

Or manually execute the SQL commands in `database.sql` using your MySQL client.

### 5. Configure Database Connection

Edit `app.py` and update the MySQL configuration:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_mysql_username'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'nearfix'
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 📁 Project Structure

```
nearfix/
├── app.py                 # Main Flask application
├── database.sql           # MySQL database schema
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── user_login.html   # User login
│   ├── user_register.html # User registration
│   ├── user_dashboard.html # User dashboard
│   ├── helper_login.html  # Helper login
│   ├── helper_register.html # Helper registration
│   ├── helper_dashboard.html # Helper dashboard
│   ├── admin_login.html   # Admin login
│   ├── admin_dashboard.html # Admin dashboard
│   ├── admin_users.html   # User management
│   ├── admin_helpers.html # Helper management
│   └── admin_services.html # Service management
└── static/              # Static files
    ├── style.css        # CSS styles
    └── script.js        # JavaScript functionality
```

## 🔐 Default Credentials

### Admin Login
- **Username**: admin
- **Password**: admin123

## 🎯 How to Use

### For Users
1. Register as a user with your details
2. Login to your dashboard
3. Select service type and describe your problem
4. Enter your location (manual or auto-detect)
5. Submit request and track status
6. Nearest available helper will be assigned automatically

### For Service Providers
1. Register as a helper with your service type
2. Wait for admin approval
3. Set your availability status
4. Receive nearby service requests automatically
5. Accept/reject requests and update status

### For Admins
1. Login with admin credentials
2. Approve pending helper registrations
3. Manage users, helpers, and services
4. Monitor all system activities
5. View comprehensive statistics

## 🌟 Key Features Explained

### Location-based Matching
- Uses Haversine formula to calculate distances
- Automatically assigns nearest available helper
- Supports manual location entry or GPS detection

### Request Status Flow
1. **Pending**: Request submitted, awaiting assignment
2. **Accepted**: Helper assigned and confirmed
3. **In Progress**: Helper started working
4. **Completed**: Service finished successfully
5. **Cancelled**: Request cancelled by user/helper

### Security Features
- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- SQL injection prevention

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Interface**: Clean, professional design
- **Interactive Elements**: Smooth animations and transitions
- **Real-time Updates**: Flash messages for user feedback
- **Accessibility**: Semantic HTML and proper labeling

## 🔧 Customization

### Adding New Services
1. Login as admin
2. Go to Services management
3. Add new service with name and description

### Modifying Service Types
Edit the `services` table in MySQL:
```sql
INSERT INTO services (service_name, description) 
VALUES ('New Service', 'Description of the new service');
```

### Changing Location Algorithm
The distance calculation is in `app.py`:
```python
def calculate_distance(lat1, lon1, lat2, lon2):
    # Modify this function to change matching algorithm
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL server is running
   - Verify database credentials in app.py
   - Ensure database exists

2. **Import Error**
   - Activate virtual environment
   - Install all requirements: `pip install -r requirements.txt`

3. **Location Not Working**
   - Enable location services in browser
   - Check HTTPS (geolocation requires secure context)
   - Try manual location entry

4. **Admin Login Not Working**
   - Verify admin record exists in database
   - Check password matches database entry

## 📱 Mobile Compatibility

The application is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Tablet devices
- Mobile phones (iOS and Android)

## 🚀 Deployment

### For Production
1. Set environment variables for database config
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure proper HTTPS
4. Set up proper database security
5. Configure firewall and security settings

### Environment Variables
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=your_user
export MYSQL_PASSWORD=your_password
export MYSQL_DB=nearfix
export SECRET_KEY=your_secret_key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For support and queries:
- Check the troubleshooting section
- Review the code comments
- Test with the provided examples

## 🎓 Educational Value

This project demonstrates:
- Full-stack web development
- Database design and management
- User authentication and authorization
- Location-based services
- RESTful API design
- Responsive web design
- Real-world application development

Perfect for college projects and portfolio building!
