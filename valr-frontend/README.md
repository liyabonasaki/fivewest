
## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.


### Deployment and Containerization

navigate to valr-frontend home directory and run the below commands

### `DOCKER_BUILDKIT=1 docker build -t valr-frontend .`
### `docker run -d -p 3000:80 valr-frontend`

