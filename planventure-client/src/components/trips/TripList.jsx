import { useState, useEffect, useCallback } from 'react';
import { Typography, Button } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { Add as AddIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import TripCard from './TripCard';
import { tripService } from '../../services/tripService';

const LoadingState = () => (
  <Grid container spacing={3}>
    {[1, 2, 3].map((skeleton) => (
      <Grid key={skeleton} size={{ xs: 12, sm: 6, md: 4 }}>
        <TripCard loading />
      </Grid>
    ))}
  </Grid>
);

const AddTripCard = ({ onAddTrip }) => (
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>
    <Button
      variant="outlined"
      fullWidth
      sx={{
        height: '100%',
        minHeight: 151.18,
        minWidth: 234.66,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
      onClick={onAddTrip}
    >
      <AddIcon sx={{ mb: 1 }} />
      <Typography>Add New Trip</Typography>
    </Button>
  </Grid>
);

const TripList = ({ WelcomeMessage, ErrorState, onRetry }) => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const fetchTrips = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await tripService.getAllTrips();

      if (!data || !data.trips) {
        throw new Error('Unexpected data format received');
      }

      setTrips(data.trips);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTrips();
  }, [fetchTrips]);

  if (loading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState onRetry={onRetry ?? fetchTrips} />;
  }

  if (trips.length === 0) {
    return <WelcomeMessage />;
  }

  return (
    <Grid container spacing={3}>
      {trips.map((trip) => (
        <Grid
          key={trip.id}
          size={{ xs: 12, sm: 6, md: 4 }}
          sx={{ minWidth: 234.66 }}
        >
          <TripCard trip={trip} />
        </Grid>
      ))}

      <AddTripCard onAddTrip={() => navigate('/trips/new')} />
    </Grid>
  );
};

export default TripList;
