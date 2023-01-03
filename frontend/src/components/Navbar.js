import { Box, Link, MenuList, MenuButton, Menu, MenuItem } from "@chakra-ui/react"
import { Link as RouterLink } from "react-router-dom"

import { useState } from "react";
import { useEffect } from "react";
const PublicNavbar = () => {

  const [user, setUser] = useState();

  useEffect(() => {
    const curUser = localStorage.getItem("user");
    console.log(curUser);
    if (curUser) {
      const getUser = JSON.parse(curUser);
      setUser(getUser.first_name);
    }
  }, []);

  const createMenu = () => {
    return (
      <Menu>
        <MenuButton color="white" borderColor="white">
          Profile
        </MenuButton>
        <MenuList>
          <MenuItem>{user}</MenuItem>
          <MenuItem onClick={handleLogout}>Logout</MenuItem>
        </MenuList>
      </Menu>
    )
  }

  const handleLogout = () => {
    setUser();
    localStorage.clear();
  }

  return (
    <Box 
      display="flex" 
      alignItems="center" 
      justifyContent="space-between" 
      px={5} py={4}
      bg="gray.900"
      borderBottom={1}
      borderColor="gray.200"
      borderStyle="solid"
    >
      <Box>
        <RouterLink to="/">
          <Link fontWeight="semibold" color="white">ApartmentSeeker</Link>
        </RouterLink>
          
      </Box>
      <Box>
        {user ? createMenu() : 
        <>
          <RouterLink to="/login">
          <Link pr={4} color="whiteAlpha.900" >Login</Link>
          </RouterLink>
        <RouterLink to="/signup">
          <Link color="whiteAlpha.900">Signup</Link>
         </RouterLink>
        </>
        }
        
      </Box>
    </Box>
  )
}

export default PublicNavbar