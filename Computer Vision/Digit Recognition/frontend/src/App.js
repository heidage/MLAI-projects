import {useState, useEffect,useRef} from 'react';
import axios from 'axios';
import './App.css';
import 'fontsource-roboto';
import Typography from '@mui/material/Typography'
import AppBar from '@mui/material/AppBar'
import ToolBar from '@mui/material/Toolbar'
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'
import Grid from '@mui/material/Grid'
import CssBaseline from "@mui/material/CssBaseline";
import {ThemeProvider, createTheme} from '@mui/material/styles';
import { makeStyles } from '@mui/styles';
import { blue, red } from '@mui/material/colors';
import Brightness6Icon from '@mui/icons-material/Brightness6';

const useStyles = makeStyles({
  root:{
    flexGrow: 1,
  },
  title:{
    textAlign: 'center',
  },
  subtitle:{
    textAlign: 'center',
  },
  buttonContainer:{
    marginBottom: '20px',
  },
  navHeader:{
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  heading:{
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 5,
  },
  toggle:{
    marginTop: 10,
  },
  body:{
    width: '60%',
    marginBottom: 20,
  }
})

const DarkTheme = createTheme({
  palette: {
    primary: {
      main: red[500]
    },
    secondary: {
      main: blue[400]
    },
    background: {
      default: '#282c34',
    },
    text: {
      primary: '#fff',
    },
  }
})

const LightTheme = createTheme({
  palette: {
    primary: {
      main: blue[500]
    },
    secondary: {
      main: red[400]
    },
    background: {
      default: '#fff',
    },
    text: {
      primary: '#282c34',
    },
  }
})

function App() {
  const classes = useStyles();
  const canvasRef = useRef(null);
  const[imageData, setImageData] = useState("");
  const[response, setResponse] = useState("Loading...");
  const[theme, setTheme] = useState(true);
  const [isDrawing, setIsDrawing] = useState(false);
  const [lastX, setLastX] = useState(0);
  const [lastY, setLastY] = useState(0);
  const appliedTheme = theme ? LightTheme : DarkTheme;

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.lineWidth = 30;
  }, []);

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  };

  const recognizeDigit = () => {
    const canvas = canvasRef.current;
    const imageBase64 = canvas.toDataURL()

    // Send the image data to the server
    axios
      .post(`http://127.0.0.1:5000/process_image`,{
          image:imageBase64,
      })
      .then((res) => {
        setResponse(res.data.image_prediction);
      });
  };

  const handleMouseDown = (e) => {
    setIsDrawing(true);
    setLastX(e.nativeEvent.offsetX);
    setLastY(e.nativeEvent.offsetY);
  };

  const handleMouseMove = (e) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const x = e.nativeEvent.offsetX;
    const y = e.nativeEvent.offsetY;
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.strokeStyle =  '#ff0000'
    ctx.stroke();
    setLastX(x);
    setLastY(y);
  };

  const handleMouseUp = () => {
    setIsDrawing(false);
  };


  return (
    <ThemeProvider theme={appliedTheme}>
      <CssBaseline />
      <div className="container">
        <div className={classes.root}>
          <AppBar>
            <ToolBar>
              <Grid justify={"space-between"} container>
                <Grid xs={1} item></Grid>
                <Grid xs={4} item>
                  <Grid container justify={"center"}>
                    <div className={classes.heading}>
                      <Typography variant="h4">
                        AI Digits
                      </Typography>
                      <Typography variant="subtitle1">
                        A rudimentary take on Neural Networks
                      </Typography>
                    </div>
                  </Grid>
                </Grid>
                <IconButton
                  onClick={() => setTheme(!theme)}
                  className={classes.toggle}
                >
                  <Brightness6Icon />
                </IconButton>
              </Grid>
              </ToolBar>
          </AppBar>
        </div>    
        <Typography variant="body1" className={classes.body} align="justify">
          As a side project in artificial intelligence, I created a 2 layer Convolutional Neural Network using tensorflow in Python. I decided to turn it into a web application with React and Flask. It's not the greatest model, but it's a decent attempt. As a 28x28 input image, the net has 784 input nodes, 2 Convolutional layers, 1 Dense Layer with 128 neurons and 10 output nodes. The canvas below is a bit less accurate since it's a 280x280 canvas scaled down and redrawn with the back-end. With the MNIST database, the neural network hits about 97-98% accuracy.
        </Typography>
        <Typography>
          Draw a digit from 0-9
        </Typography>
        <div className="canvas">
          <canvas
            ref={canvasRef}
            width={280}
            height={280}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
          />
        </div>
        <div className={classes.buttonContainer}>
          <Button 
            onClick={clearCanvas}
            color="secondary"
            variant="outlined"
          >
            Reset
          </Button>
          <Button 
            onClick={recognizeDigit}
            color="primary"
            variant="outlined"
          >
            Guess
          </Button>
        </div>
        <Typography variant="h5">
          Your number is {response}
        </Typography>
      </div>
    </ThemeProvider>
  );
}

export default App;