# Live Shift Countdown Timer

A professional, real-time countdown display showing how much time remains before a care worker's shift ends.

## Features

### Live Countdown Display
- **Real-time clock format**: HH:MM:SS updating every second
- **Elegant design**: Clean typography with monospace font for precision
- **Professional styling**: Gradient backgrounds, soft transitions, and blurred effects
- **Pulsing alert**: Automatic highlighting when 1 hour or less remains in shift
- **Responsive layout**: Works seamlessly on desktop, tablet, and mobile devices

### Shift Information Display
- Current shift type (Day/Night)
- Shift start and end times
- Progress bar showing percentage of shift completed
- Percentage indicator
- Custom notes field

### Smart Time Management
- Automatically detects shift type (7am-7pm vs 7pm-7am)
- Handles night shift timing correctly (crossing midnight)
- Displays countdown in hours:minutes:seconds format
- Updates API data every 5 minutes for fresh information

## How It Works

### Backend Architecture

**UserShift Model** (`dashboard/models.py`)
- One-to-one relationship with User model
- Stores shift type, start time, end time, and date
- Calculated properties for:
  - `time_remaining_minutes`: Minutes until shift end
  - `time_remaining_formatted`: HH:MM format
  - `shift_progress_percent`: 0-100 percentage

**API Endpoints**

1. **GET /api/shifts/current/**
   - Returns current user's active shift
   - Falls back to default shift if none exists
   - Includes time remaining and progress information

2. **POST /api/shifts/set/**
   - Create or update user's shift
   - Parameters:
     - `shift_type`: 'day', 'night', or 'custom'
     - `start_time`: Time in HH:MM format
     - `end_time`: Time in HH:MM format
     - `notes`: Optional shift notes

### Frontend Countdown Logic

1. **Initialization**: Reads shift end time from dashboard
2. **Calculation**: Computes time remaining every second
3. **Update**: Updates all countdown values simultaneously
4. **Styling**: Applies pulsing effect when <1 hour remaining
5. **API Sync**: Refreshes from server every 5 minutes

## Usage

### For Care Workers/Staff

The countdown timer appears on the main dashboard as soon as you log in. It shows:
- How much time is left in your shift (HH:MM:SS format)
- Your shift times (start and end)
- Progress through the shift as a percentage
- Shift type (Day/Night)

No action needed - it updates automatically!

### For Administrators

#### Setting a User's Shift via Admin Panel

1. Go to: `/admin/dashboard/usershift/`
2. Click "Add User Shift"
3. Fill in:
   - **User**: Select the care worker
   - **Shift Type**: Day, Night, or Custom
   - **Start Time**: e.g., 07:00
   - **End Time**: e.g., 19:00
   - **Is Active**: Check if currently active
   - **Notes**: Optional notes (e.g., "Covering for Sarah")
4. Click "Save"

#### Via API (Programmatic)

```bash
curl -X POST http://localhost:8000/api/shifts/set/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "shift_type": "day",
    "start_time": "07:00",
    "end_time": "19:00",
    "notes": "Standard day shift"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Shift scheduled successfully",
  "shift_type": "day",
  "start_time": "07:00",
  "end_time": "19:00",
  "time_remaining_minutes": 285,
  "time_remaining_formatted": "04:45"
}
```

#### Retrieving Current Shift Info

```bash
curl -X GET http://localhost:8000/api/shifts/current/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "user": "jane_smith",
  "shift_type": "day",
  "start_time": "07:00",
  "end_time": "19:00",
  "time_remaining_minutes": 285,
  "time_remaining_formatted": "04:45",
  "progress_percent": 68,
  "notes": "Standard day shift"
}
```

## Shift Types

### Day Shift (7am - 7pm)
- 12 hours
- Standard working hours
- Common for care assistants and nurses

### Night Shift (7pm - 7am)
- 12 hours
- Overnight care coverage
- Special handling for midnight crossing

### Custom Hours
- Set any start and end time
- Useful for part-time staff or split shifts
- Example: 10:00 - 16:00 (6 hours)

## Visual Design

### Color Scheme
- **Day Shift**: Bright blue gradient background
- **Night Shift**: Dark purple/indigo gradient
- **Text**: High contrast white text for readability
- **Progress Bar**: Animated fill showing shift progression

### Responsive Behavior
- **Desktop**: Two-column layout (countdown + progress info)
- **Tablet**: Stacked layout with full width
- **Mobile**: Vertical stacking with adjusted font sizes

### Dark Mode Support
- Automatically adjusts colors based on dark mode setting
- Maintains readability in both light and dark themes
- Smooth transitions when toggling dark mode

## Pulsing Alert Feature

When 1 hour or less remains in the shift:
- Countdown timer pulses with a soft glow effect
- Visual cue without being intrusive
- Helps staff prepare for shift handover

## Database Schema

### UserShift Table

```sql
CREATE TABLE dashboard_usershift (
  id INTEGER PRIMARY KEY,
  user_id INTEGER UNIQUE NOT NULL,
  shift_type VARCHAR(20),
  start_time TIME,
  end_time TIME,
  shift_date DATE,
  is_active BOOLEAN,
  notes TEXT,
  created_at DATETIME,
  updated_at DATETIME
);
```

## Technical Details

### Time Calculation

The countdown uses JavaScript's native `Date` object:

```javascript
const now = new Date();
const shiftEnd = new Date();
shiftEnd.setHours(endHours, endMinutes, 0, 0);

const diff = shiftEnd - now; // milliseconds remaining
const hours = Math.floor(diff / (1000 * 60 * 60));
const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
const seconds = Math.floor((diff % (1000 * 60)) / 1000);
```

### Night Shift Logic

For night shifts crossing midnight:
```javascript
if (shiftEnd < now) {
  shiftEnd.setDate(shiftEnd.getDate() + 1);
}
```

This ensures the countdown doesn't display negative values at the start of a night shift.

### Server-Side Calculation

Python backend also calculates time remaining:
```python
@property
def time_remaining_minutes(self):
    now = timezone.now()
    delta = self.shift_end_datetime - now
    return int(delta.total_seconds() / 60)
```

## Troubleshooting

### Timer Not Updating
- Check browser console for JavaScript errors
- Ensure JavaScript is enabled
- Clear browser cache and refresh page

### Incorrect Time Remaining
- Verify server time is correct: `date`
- Check user's shift is active in admin panel
- Ensure timezone is set correctly in settings.py

### API Not Responding
- Verify user is authenticated
- Check API endpoint URL is correct
- Look for error messages in Django logs

### Shift Not Saving
- Ensure user is not already assigned a shift for that date
- Check unique constraint: `unique_together = ['user', 'shift_date']`
- Verify all required fields are provided

## Customization

### Change Shift Times in Admin

Edit `/admin/dashboard/usershift/` to customize:
- Default shift start/end times
- Shift type options
- Display format

### Customize Appearance

Edit CSS in `templates/dashboard/dashboard.html`:
- `.countdown-display`: Font size, color, styling
- `.countdown-timer`: Background, border radius
- `.shift-status-card.day-shift`: Day shift colors
- `.shift-status-card.night-shift`: Night shift colors

### Adjust Update Frequency

In dashboard.html JavaScript:
```javascript
// Change 5 minutes (300000 ms) to desired interval
setInterval(updateShiftFromAPI, 5 * 60 * 1000);

// Change 1 second (1000 ms) for countdown updates
setInterval(updateCountdown, 1000);
```

## Production Notes

- Timer displays in browser's local timezone
- Ensure Django `TIME_ZONE` setting matches facility timezone
- All shifts reset at midnight
- API returns ISO 8601 timestamps for reliability
- Countdown continues even if API connection is lost (uses cached time)

## Future Enhancements

Potential improvements:
- Break time tracking within shift
- Overtime indication
- Automatic shift notifications at key milestones
- Bulk shift scheduling for multiple staff
- Mobile app integration
- SMS/email shift reminders
- Shift swap requests UI

## Support

For issues or feature requests:
1. Check this documentation
2. Review Django logs: `python manage.py runserver`
3. Inspect browser console for JavaScript errors
4. Check API responses in Network tab

---

**Created**: 2026-05-18  
**Version**: 1.0  
**Status**: Production Ready
