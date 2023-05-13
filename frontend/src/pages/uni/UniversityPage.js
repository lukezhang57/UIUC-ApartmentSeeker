import React, { useEffect, useState } from 'react'
import Navbar from '../../components/Navbar'
import { 
  Box, Container, Select, NumberInput, NumberInputField, 
  NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper,
   Text, Heading, Tag, Image, Button, Badge, Flex,
   Grid, FormControl, GridItem, HStack, Link, FormLabel, VStack, Tooltip, Skeleton, Stack, filter
} from '@chakra-ui/react'
import { useNavigate, useLocation, useParams } from 'react-router'
import { ExternalLinkIcon, Icon, StarIcon } from '@chakra-ui/icons'
import { Input } from '@chakra-ui/react'
import tmpData from '../../tmpData/apartments'
import axios from 'axios'
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import MapHelper from './MapHelper'
import Multiselect from 'multiselect-react-dropdown';

const University = () => {

  const [fullList, setFullList] = useState()
  const [uni, setUni] = useState()
  const [sorted, setSorted] = useState()


  const [uniDetails, setUniDetails] = useState()
  const location = useLocation()
  const { id } = useParams()
  const uni_slug = location.pathname.split('/')[2]



  const [minRating, setMinRating] = useState(0)
  const filterThreshhold = 700

  


  useEffect(() => {

    const getData = async () => {
      console.log('trying to add stuff')
      try {
        const res = await axios.get(
          `http://localhost:8000/api/get_university_apartments?university_slug=${uni_slug}&starting_index=${0}&ending_index=${5}`
        )
        console.log(res.data)
        setUni(res.data)
        setSorted(res.data)
        setFullList(res.data)


        const detailsRes = await axios.get(
          `http://localhost:8000/api/get_university_data?university_slug=${uni_slug}`
        )
        console.log('details', detailsRes.data)
        setUniDetails(detailsRes.data)

        setBuildings(detailsRes.data.important_buildings)
        console.log('setting buildings to ', detailsRes.data.important_buildings)

      } catch (e) {
        console.log('error: ' + e)
      }
    }
    getData()
  },[])


  // STATE / FUNCTIONS FOR IMPORTANT BUILDINGS
  const [buildings, setBuildings] = useState([])
  const [selectedBuildings, setSelectedBuildings] = useState([])

  const onSelect = (selectedList, selectedItem) => {
    let buildingToPush = null
    for (let i = 0; i < buildings.length; i++) {
      console.log('comparing ' + buildings[i].building_name + ' and ' + selectedItem.building_name)
      if (buildings[i].building_name === selectedItem.building_name) {
        buildingToPush = buildings[i];
        break;
      }
    }
    console.log('adding', buildingToPush)
    setSelectedBuildings([...selectedBuildings, buildingToPush])
  }

  const onRemove = (selectedList, removedItem) => {
    setSelectedBuildings(selectedBuildings.filter(b => b.building_name !== removedItem.building_name))
  }


  // STATE / FUNCTIONS FOR distance/time values

  const [maxWalkingDist, setMaxWalkingDist] = useState("-1");
  const [maxBikingDist, setMaxBikingDist] = useState("-1");
  const [maxDrivingDist, setMaxDrivingDist] = useState("-1");
  const [maxTransitTime, setMaxTransitTime] = useState("-1");


  return (
    <>
      <Navbar />
        <Stack mt={4} display={(uni && uniDetails && buildings) && "none"}>
          <Skeleton isLoaded={(uni && uniDetails && buildings)} height='20px' />
          <Skeleton isLoaded={(uni && uniDetails && buildings)} height='20px' />
          <Skeleton isLoaded={(uni && uniDetails && buildings)} height='20px' />
        </Stack>
        
        {(uni && uniDetails && buildings) ? 
          (<Box pt={2} mt={2} d="flex" flexDir="column" justifyContent="center" alignItems="center">
            <Flex maxW="container.xl">

            
              <Container maxWidth="container.xl" flex={2}>
                <Box 
                  display="flex" 
                  alignItems="center" 
                  py={4}
                  bg="white"
                  boxShadow="md"
                  pl={6}
                  pr={2}
                >
                  <Box>
                    <Image w={150} h={150} borderRadius="full" alt="school-image" src={uniDetails.img_url} />
                  </Box>
                  <Box ml={5}>
                    <Text color="gray.600" fontWeight="semibold" fontSize="lg">Apartments located at</Text>
                    <Heading size="lg">
                      {uniDetails.name}
                    </Heading>
                    <Box display="flex" alignItems="center" mt={2}>
                      <Box color="blue.600" textTransform="uppercase" fontWeight="bold">
                        {uniDetails.address.city}
                      </Box>
                      <Link isExternal ml={2} color="gray.700" href={uniDetails.website_url}>
                        Visit School Website <ExternalLinkIcon mx='2px' />
                      </Link>             
                    </Box>
                    {/* <HStack mt={1}>
                      <Text fontSize="sm" color="gray.700">44,087 students</Text>
                      <Text  fontSize="sm" color="gray.700">Dorms required for <strong>Freshmen</strong></Text>
                    </HStack> */}
                    {/* <HStack spacing={2} mt={2}>
                      <Badge colorScheme="green">Public Institution</Badge>
                      <Badge colorScheme="blue">Large Student Body</Badge>
                      <Badge colorScheme="red">State School</Badge>
                    </HStack> */}
                  </Box>
                </Box>
                <Grid>
                </Grid>
              </Container>
            </Flex>
            
            
            <Flex maxW="container.xl">
              <Container maxWidth="container.xl" mt={2}>
                <MapContainer center={[uniDetails.address.lat, uniDetails.address.long]} zoom={13} style={{"height": "100%", "width": "100%"}}>
                  <MapHelper />
                  <TileLayer 
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  />
                  {selectedBuildings.map((building) => (
                    <Marker position={[building.address.lat, building.address.long]}>
                      <Popup>
                        {building.building_name}
                      </Popup>
                    </Marker>
                  ))}
                </MapContainer>
                <Box d="flex" mb={2} bg="white" padding={2} boxShadow="md" ml={2}>
                  <Box border='1px' borderColor='gray' d="flex" alignItems="center" ml={2}>
                    <Stack spacing={3}>
                      <FormLabel fontSize="sm">Maximum Preferred Walking Distance</FormLabel>
                      <NumberInput value={maxWalkingDist} precision={2} step={0.2}
                        onChange={(valueString) => setMaxWalkingDist(valueString)}>
                        <NumberInputField />
                        <NumberInputStepper>
                          <NumberIncrementStepper />
                          <NumberDecrementStepper />
                        </NumberInputStepper>
                      </NumberInput>
                      <FormLabel fontSize="sm">Maximum Preferred Biking Distance</FormLabel>
                      <NumberInput value={maxBikingDist} precision={2} step={0.2}
                        onChange={(valueString) => setMaxBikingDist(valueString)}>
                        <NumberInputField />
                        <NumberInputStepper>
                          <NumberIncrementStepper />
                          <NumberDecrementStepper />
                        </NumberInputStepper>
                      </NumberInput>
                      <FormLabel fontSize="sm">Maximum Preferred Driving Distance</FormLabel>
                      <NumberInput value={maxDrivingDist} precision={2} step={0.2}
                        onChange={(valueString) => setMaxDrivingDist(valueString)}>
                        <NumberInputField />
                        <NumberInputStepper>
                          <NumberIncrementStepper />
                          <NumberDecrementStepper />
                        </NumberInputStepper>
                      </NumberInput>
                      <FormLabel fontSize="sm">Maximum Preferred Transit Time</FormLabel>
                      <NumberInput value={maxTransitTime} precision={2} step={0.2}
                        onChange={(valueString) => setMaxTransitTime(valueString)}>
                        <NumberInputField />
                        <NumberInputStepper>
                          <NumberIncrementStepper />
                          <NumberDecrementStepper />
                        </NumberInputStepper>
                      </NumberInput>
                    </Stack>
                  </Box>
                <Multiselect
                  style={{ multiselectContainer: { width: "700px" } }}
                  options={buildings} // Options to display in the dropdown
                  selectedValues={selectedBuildings} // Preselected value to persist in dropdown
                  onSelect={onSelect} // Function will trigger on select event
                  onRemove={onRemove} // Function will trigger on remove event
                  displayValue="building_name" // Property name to display in the dropdown options
                  />
                  <Button 
                    ml={2} 
                    colorScheme="blue"
                    onClick={(e) => {
                      e.preventDefault()
                      let string = '['
                      for (let i = 0; i < selectedBuildings.length; i++) {
                        if (i != selectedBuildings.length - 1) {
                          string += '"' + selectedBuildings[i].building_slug + '"' + ', '
                        }  else {
                          string += '"' + selectedBuildings[i].building_slug + '"'
                        }
                        
                      }
                      string += ']'
                      console.log('string: ' , string)

                      const getData = async () => {
                        try {
                          const res = await axios.get(
                            `http://localhost:8000/api/get_nearest_apartments?universitySlug=${uni_slug}&buildingSlugs=${string}&starting_index=${0}&ending_index=${50}&minWalkingDist=${maxWalkingDist}&minBikingDist=${maxBikingDist}&minDrivingDist=${maxDrivingDist}&maxTransitTime=${maxTransitTime}`
                          )
                          console.log('received: ' ,res.data)
                          setUni(res.data)
                          setSorted(res.data)
                        } catch (e) {
                          console.log(e)
                        }
                      }
                      getData()
                      
                      
            
                    }}
                  >
                    Find
                  </Button>
                  {/* <Box d="flex" alignItems="center" ml={2}>
                    <Tooltip label="Find apartments within a 1 mile radius of these buildings">
                      <Box color="gray.500">
                        What is this?
                      </Box>
                    </Tooltip>
                  </Box> */}
                  
                
                  
                </Box>
                <Grid templateColumns='repeat(6, 1fr)' gap={3}>
                  <GridItem colSpan={1}>
                    <Box bg="white" boxShadow="md" px={3} py={4}>
                      <VStack alignItems="left">
                        <Heading size="xs" mb={2}>
                          Apply Filters
                        </Heading>
                        <FormControl>
                          <FormLabel fontSize="sm">Price Range</FormLabel>
                          <Select size="xs" onChange={(e) => {
                            console.log(e.target.value)
                            if (e.target.value === 'any') {
                              setSorted(fullList)
                            } else if (e.target.value === 'below') {
                              let filtered = uni.filter(item => item.min_cost <= 700)
                              console.log('filtered', filtered)
                              setSorted(filtered)
                            } else if (e.target.value === 'above') {
                              let filtered = uni.filter(item => item.min_cost > 700)
                              console.log('filtered', filtered)
                              setSorted(filtered)
                            }
                          }}>
                            <option value='any'>Any Price</option>
                            <option value='below'>$700 and Below</option>
                            <option value='above'>$701 and Above</option>
                          </Select>
                        </FormControl>
                        <FormControl>
                          <FormLabel fontSize="sm">Minimum Overall Rating</FormLabel>
                          <NumberInput 
                            size="xs" 
                            defaultValue={0} 
                            min={0} 
                            max={5}
                            
                          >
                            <NumberInputField onChange={(e) => {
                              console.log(e.target.value)
                              
                              
                                let filtered = sorted.filter(uni => uni.overall_rating > e.target.value)
                                setSorted(filtered)
                              
                              

                            }} />
                          </NumberInput>
                        </FormControl>

                      </VStack>
                      <Button 
                        mt={2} 
                        size="sm" 
                        colorScheme="blue"
                        onClick={(e) => {
                          setSorted(fullList)
                        }}
                      >
                        Reset
                      </Button>
                    </Box>
                  </GridItem>
                  <GridItem colSpan={5}>
                    {/* For the reviews */}
                    <Grid templateColumns='repeat(4, 1fr)' gap={2}>
        
                      {sorted.map((a) => (
                        <Box width="100%" bg="white" boxShadow="md" key={a.id}>
                        <Image width="100%" objectFit="cover" height={250} alt="ucla" src={a.img_url} />
                        <Box px={3} py={3}>
                          <Text textTransform="uppercase" fontWeight="bold" fontSize="xs">
                            {a.address.address1}
                          </Text>
                          <Heading size="md">
                            {a.apartment_name}
                          </Heading>
                          <Box mt={1} d="flex">
                            <HStack spacing={1}>
                              {(function generateStars() {
                                  let result = []
                                  let counter = 0;
                                  for (let i = 0; i < a.overall_rating; i++) {
                                    result.push(<StarIcon boxSize={3} color="yellow.300" />)
                                    counter++
                                  }
                                  for (let j = 0; j < 5 - counter; j++) {
                                    result.push(<StarIcon boxSize={3} color="gray.300" />)
                                  }
                                  return result
                                })()}
                            </HStack>
                            <Text ml={2} color="gray.500" fontSize="xs">Overall {a.overall_rating}/5</Text>
                          </Box>
                          <Text color="gray.600" fontSize="xs" mt={1}>
                            17 total reviews
                          </Text>
                          <Box>
                            <Link href={`/apartments/reviews/${a.apartment_slug}`}> 
                              <Button 
                                mt="2" 
                                size="xs" 
                                width="100%" 
                                color="white" 
                                bg="teal.500"
                                _hover={{ bg:"teal.400" }}
                              >
                                Browse Reviews
                              </Button>
                            </Link>
                            <Link href={`/apartments/sublease/${a.apartment_slug}`}> 
                              <Button 
                                mt="2" 
                                size="xs" 
                                width="100%" 
                                colorScheme="blue"
                                _hover={{ bg:"teal.400" }}
                              >
                                View Subleases
                              </Button>
                            </Link>
                          </Box> 
                          
                        </Box>
                      </Box>

                      ))}  
                    </Grid>
                  </GridItem>

                </Grid>
              </Container>  
            </Flex>
          </Box>) : <div>Loading ...</div> }
        

    </>
  )
}

export default University

