import { Container, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          mt: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to Quiz App
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Test your knowledge with our interactive quizzes!
        </Typography>
        <Box sx={{ mt: 4 }}>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate('/questions')}
            sx={{ mr: 2 }}
          >
            View Questions
          </Button>
          <Button
            variant="outlined"
            color="primary"
            size="large"
            onClick={() => navigate('/add-question')}
          >
            Add New Question
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Home; 