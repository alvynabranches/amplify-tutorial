// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

import { useEffect } from "react";
import { API } from "aws-amplify";

const api = "alvynapi";

function App() {
  useEffect(() => {
    const getData = async () => {
      const data = await API.get(api, "/song");
      console.log(data);
    }
  getData();
  });

  // useEffect(() => {
  //   const getData = async () => {
  //     const data = await API.post(api, "/song", {
  //       body: {
  //         name: "Toxic", 
  //         year: 2003,
  //         link: "http://www.random.com"
  //       }
  //     });
  //     console.log(data);
  //   }
  // getData();
  // });
  return <div></div>
}

export default App;