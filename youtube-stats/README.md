## Instructions to run
1. Clone repository
2. Run npm install to install node modules
3. Add your API key in the .env file (replace YOURAPIKEY with your real API Key). Instructions to obtain API key found [here](https://www.slickremix.com/docs/get-api-key-for-youtube/)
4. Run npm start to run app
5. Insert YouTube Video ID into search box and hit enter to retrieve results. You can get the video ID from any YouTube video URL. 

## Instructions to Build and Run Docker Image
1. Follow instructions 1 & 3 above.
2. To build image, cd into directory and run `docker build . -t youtubereactapp:latest`
3. To run container enter `docker run --rm -it -p 3000:3000/tcp youtubereactapp:latest`

## Generic Create React App Stuff
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `yarn test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

