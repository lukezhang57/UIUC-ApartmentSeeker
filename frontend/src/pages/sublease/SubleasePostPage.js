import React, { useEffect } from 'react'
import Navbar from '../../components/Navbar'
import { 
  Box, Container, Heading, Button, Text,
  Stack, Grid, FormControl, FormLabel, Flex, Input, Textarea, useToast
} from '@chakra-ui/react'
import Sublease from '../../components/Sublease'
import axios from 'axios'
import { useLocation, useNavigate, Navigate } from 'react-router'
import { useState } from 'react'



const Subleases = () => {
  const location = useLocation()
  const apartment_slug = location.pathname.split('/')[4]

  let navigate = useNavigate()

  const [redirect, setRedirect] = useState(false)

  const [subleases, setSubleases] = useState()


  let user = JSON.parse(localStorage.getItem("user"))


  const [details, setDetails] = useState()
  const [price, setPrice] = useState()
  const [beds, setBeds] = useState() 
  const [baths, setBaths] = useState()

  const [loading, setLoading] = useState(false)

  const toast = useToast()
  
    

  useEffect(() => {
    const getData = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/get_apartment_subleases?apartment_slug=${apartment_slug}`)
        console.log('response data: ', res.data)
        setSubleases(res.data)
      } catch (e) {
        console.log(e)
      }
    }
    getData()
    
  },[])
  

  if (redirect) {
    return <Navigate replace to={`/apartments/sublease/${apartment_slug}`} />
  }

  return (
    <>
      <Navbar />
      {subleases && 
      (<>
       <Flex justify="center" align="center" minHeight="100vh" bg="gray.50">
          <Stack spacing="10">
          
          <Stack align="center">
            <Heading fontWeight="semibold">
              Submitting Sublease for {' '}
              {subleases.length > 0 ?  subleases[0].associated_apartment.apartment_name : apartment_slug}
            </Heading>
          </Stack>
          <Box bg="white" py="10" px="7" rounded="lg" boxShadow="lg">
            <Stack>
              <Text mb={4}>Note: your potential tenants will be able to see your contact information.</Text>
              <FormControl>
                <FormLabel htmlFor="email">Expected Price Monthly Rent</FormLabel>
                <Input 
                  id="price" 
                  type="text" 
                  onChange={(e) => {
                    setPrice(e.target.value)
                  }}
                />
              </FormControl>

              <FormControl mb={4}>
                <FormLabel htmlFor="email">Number of Beds</FormLabel>
                <Input 
                  placeholder='Enter number of beds' 
                  onChange={(e) => {
                    setBeds(e.target.value)
                  }}
                />
              </FormControl>

              <FormControl mb={4}>
                <FormLabel htmlFor="email">Number of Baths</FormLabel>
                <Input 
                  placeholder='Enter number of baths' 
                  onChange={(e) => {
                    setBaths(e.target.value)
                  }}
                />
              </FormControl>

              <FormControl>
                <FormLabel htmlFor="email">Add More Details</FormLabel>
                <Textarea 
                  placeholder='Enter any details here ...' 
                  onChange={(e) => {
                    setDetails(e.target.value)
                  }}
                />
              </FormControl>

              
              
            </Stack>
            <Button 
              color="white" 
              bg="blue.500" 
              mt="5" 
              w="100%"
              _hover={{ bg:"blue.400" }}
              isLoading={loading}
              onClick={(e) => {
                setLoading(true)
                if (user) {
                  const waitResponse = async () => {
                    try {
                      const res = await axios.post(
                        `http://127.0.0.1:8000/api/post_sublease?userName=${user.user_name}&apartmentSlug=${apartment_slug}&subleaseText=${details}&price=${price}&beds=${beds}&baths=${baths}`
                      );
                      console.log(res.data)
    
                      setRedirect(true)
                    } catch (e) {
                      console.log(e)
                    }
                  }
                  waitResponse()
                  
                } else {
                  toast({
                    title: 'You must be logged in.',
                    description: "You must log in to do that.",
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                  })
                }
                
              }}
            >
              Post
            </Button>
          </Box>
        </Stack>
      </Flex>
      </>)
  }
            
    </>
  )
}

export default Subleases