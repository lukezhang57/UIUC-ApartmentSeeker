import React from 'react';
import {
  ChakraProvider,
  theme,
} from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import {
  BrowserRouter as Router,
  Routes, Route, Link, Outlet
} from "react-router-dom"
import TestPage from './pages/TestPage'
import HomePage from './pages/HomePage'
import UniversityPage from './pages/uni/UniversityPage'
import ReviewsPage from './pages/review/ReviewsPage'
import LoginPage from './pages/auth/LoginPage'
import SignupPage from './pages/auth/SignupPage'
import SubleasePage from './pages/sublease/SubleasePage'
import SubleasePostPage from './pages/sublease/SubleasePostPage'

function App() {
  return (
    <ChakraProvider theme={theme}>
      <Router>
        <Routes>
          <Route path="/about" element={<TestPage />}>
            
          </Route>
          <Route path="/users">
            
          </Route>
          <Route path="/" element={<HomePage />}>
           
          </Route>
          <Route path="/login" element={<LoginPage />}>
          </Route>

          <Route path="/signup" element={<SignupPage />}>
          </Route>

          <Route path="university/:id" element={<UniversityPage />}></Route>
          <Route path="/apartments/reviews/:slug" element={<ReviewsPage />}></Route>


          <Route path="/apartments/sublease/:slug" element={<SubleasePage />}>
          </Route>
          <Route path="/apartments/sublease/post/:sl" element={<SubleasePostPage />}>
          </Route>
           
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;
