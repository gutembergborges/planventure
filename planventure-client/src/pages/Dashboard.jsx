import { useNavigate } from 'react-router-dom';
import { Box, Typography, Paper, Button } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import TripList from '../components/trips/TripList';
import travelingSvg from '../assets/undraw_traveling_yhxq.svg';

const IllustratedState = ({
  title,
  description,
  buttonLabel,
  onAction,
  isError = false,
  buttonStartIcon = null,
}) => (
  <Box
    sx={{
      textAlign: 'center',
      py: 6,
      px: 2,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: 3,
    }}
  >
    <img
      src={travelingSvg}
      alt={isError ? 'Error loading trips' : 'Start your journey'}
      style={{
        maxWidth: '300px',
        width: '100%',
        height: 'auto',
        marginBottom: '1rem',
        opacity: isError ? 0.7 : 1,
      }}
    />

    <Typography
      variant={isError ? 'h5' : 'h4'}
      component="h2"
      gutterBottom
    >
      {title}
    </Typography>

    <Typography
      variant="body1"
      color="text.secondary"
      sx={{ maxWidth: '600px', mb: 3 }}
    >
      {description}
    </Typography>

    <Button
      variant="contained"
      size={isError ? 'medium' : 'large'}
      startIcon={buttonStartIcon}
      onClick={onAction}
    >
      {buttonLabel}
    </Button>
  </Box>
);

const Dashboard = () => {
  const navigate = useNavigate();

  const handleCreateTrip = () => navigate('/trips/new');
  const handleRetry = () => window.location.reload();

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: { xs: 2, sm: 3 } }}>
      <Typography variant="h4" component="h1" gutterBottom>
        My Trips
      </Typography>
      <Paper
        elevation={2}
        sx={{
          p: 3,
          display: 'flex',
          flexDirection: 'column',
          minHeight: '60vh',
        }}
      >
        <TripList
          WelcomeMessage={() => (
            <IllustratedState
              title="Welcome to Planventure!"
              description="Ready to start planning your next adventure? Create your first trip and let us help you organize everything from destinations to activities."
              buttonLabel="Plan Your First Trip"
              onAction={handleCreateTrip}
              buttonStartIcon={<AddIcon />}
            />
          )}
          ErrorState={({ onRetry }) => (
            <IllustratedState
              title="Oops! Looks like our compass is spinning! 🧭"
              description="We're having trouble loading your adventures..."
              buttonLabel="Try Again"
              onAction={onRetry}
              isError
            />
          )}
        />
      </Paper>
    </Box>
  );
};

export default Dashboard;
