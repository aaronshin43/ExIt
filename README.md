> This is the [Red Devil Hackathon](https://reddevilhacks.github.io/) markdown submission template. Replace *italicized* placeholders with your project details and remove the markdown quotes as well.

> Here are some example submissions from Boosung's previous hackathons: [Frody](https://devpost.com/software/temptemp) and [Albatross](https://devpost.com/software/albatross).

# ExIt (Exchange It)
### ExIt is a web application designed specifically for Dickinson students and faculties to buy and sell items within our campus community. The application uses Flask for the backend, SQLite for the database, and includes features like user authentication, item search, and item filter.
**Team:** Aaron Shin

**Submission video:** *[Link to video.](https://youtu.be/aM8D2S3nsx4)*  
> ⏱️ The video should be 5 minutes or less. In the video, you should include the project inspiration, what it does, and a demo showcasing the key features.

> 🎥 The easiest way to make a video here would be to use OBS or Zoom for screen recording. You can upload the video as an unlisted video on YouTube and add the link here.

## Inspiration
The inspiration for ExIt came from the need to create a safe and convenient platform for Dickinson students and faculty to exchange items within the campus community. Many students face challenges in finding affordable items or selling unused belongings, and ExIt aims to solve this problem by providing a centralized marketplace.

## What it does
ExIt allows users to:
- Register and log in securely.
- Post items for sale with details like name, description, price, category, and images.
- Search for items using keywords and filter them by category or price range.
- View detailed information about items and contact sellers directly.

## How we built it
We built ExIt using:
- **Backend**: Flask (Python) for routing, user authentication, and database interactions.
- **Database**: SQLite for storing user and item data.
- **Frontend**: HTML, CSS, and Bootstrap for responsive design.
- **Authentication**: Flask-Login and bcrypt for secure user authentication.
- **File Uploads**: Flask-WTF for handling image uploads.

## Challenges & Accomplishments
### Challenges:
- Implementing secure user authentication and password hashing.
- Designing a responsive and user-friendly interface.
- Handling image uploads and ensuring proper file storage.

### Accomplishments:
- Successfully implemented a fully functional marketplace with search and filter features.
- Created a clean and minimalistic UI for users.
- Learned how to integrate Flask with SQLite and manage database relationships effectively.

## What's next?
- Add a chat feature for buyers and sellers to communicate directly within the platform.
- Implement a rating system for users to build trust within the community.
- Expand the platform to include more categories and advanced search options.
- Implement an email verification system to make sure the user owns the Dickinson email

## Try it out
*Include setup instructions so that judges (and others) can run your project locally. The judges must be able to run your application.*

```bash
# 1. Clone the repository
git clone https://github.com/aaronshin43/ExIt.git
cd ExIt

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. (Optional) Reset database with example items
python reset_db.py
```
