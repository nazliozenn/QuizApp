import { AppBar, Toolbar, Typography, Button, Container } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Container>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Quiz App
          </Typography>
          <Button color="inherit" component={RouterLink} to="/">
            Home
          </Button>
          <Button color="inherit" component={RouterLink} to="/questions">
            Questions
          </Button>
          <Button color="inherit" component={RouterLink} to="/add-question">
            Add Question
          </Button>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar; 