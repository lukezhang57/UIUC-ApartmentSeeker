import React, { useEffect } from 'react'
import Navbar from '../../components/Navbar'
import { 
  Box, Container, Heading, Grid, Button
} from '@chakra-ui/react'
import Sublease from '../../components/Sublease'
import axios from 'axios'
import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'

const Subleases = () => {

  const user = JSON.parse(localStorage.getItem("user"));
  

  const location = useLocation()
  const apartment_slug = location.pathname.split('/')[3]
  console.log('slug: ', apartment_slug, user)
  const [subleases, setSubleases] = useState()

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







  return (
    <>
      <Navbar />
      
      {subleases &&
        (<Container maxW="container.xl" mt={4}>
          <Box textAlign="center">
            <Heading>Viewing Subleases for {subleases.length > 0 ? subleases[0].associated_apartment.apartment_name : apartment_slug}</Heading>
            <Heading size="lg">{subleases[0]?.associated_apartment.apartment_name}</Heading>
          </Box>
          <Box mt={8}>

          </Box>
          { (subleases && subleases.length === 0) && <h1>Currently Empty</h1>}
          <Grid templateColumns='repeat(2, 1fr)' gap={4}>
            {
              subleases.map((sublease) => {

                return (
                  <Sublease 
                    apartment_name={sublease.associated_apartment.apartment_name} 
                    apartment_slug={sublease.associated_apartment.apartment_slug} 
                    url={sublease.associated_apartment.website_url}
                    details={sublease.sublease_text}
                    beds={sublease.beds}
                    baths={sublease.baths}
                    price={sublease.price}
                    username={sublease.tenant.user_name}
                  />
                )
                
              })
            }
          </Grid>
          <Box mt={8}>
            <Link to={`/apartments/sublease/post/${apartment_slug}`}>
              <Button colorScheme="green">Add Your Sublease</Button>
            </Link>
          </Box>
        </Container>)
      }
            
    </>
  )
}

export default Subleases