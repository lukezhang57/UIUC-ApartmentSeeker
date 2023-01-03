import { 
  Box, 
  Heading, 
  Button, 
  Image, 
  Grid, 
  GridItem, 
  Text, 
  Link, 
  useDisclosure,
  Modal, 
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  HStack,
  Textarea,
  useToast
} from "@chakra-ui/react"
import { ExternalLinkIcon } from "@chakra-ui/icons"
import { useState } from "react"
import axios from "axios"

const Sublease = ({ apartment_name, apartment_slug, url, details, beds, baths, price, username }) => {

  const { isOpen, onOpen, onClose } = useDisclosure()

  const { isOpen: isOpen2, onOpen: onOpen2, onClose: onClose2 } = useDisclosure()

  const user = JSON.parse(localStorage.getItem("user"));

  const [content, setContent] = useState()

  const toast = useToast()

  return (
    <Box w="100%" bg="white" boxShadow="sm" borderColor="teal.300" borderWidth={1}>
      <Box d="flex">
        {/* <Box flex={2}>
          <Image objectFit="cover" height="100%" alt="ucla" src={'google.com'} />
        </Box> */}
        <Box flex={3} p={3}>
          <Box
            color='gray.500'
            fontWeight='semibold'
            letterSpacing='wide'
            fontSize='xs'
            textTransform='uppercase'
          >
            {beds} beds &bull; {baths} baths 
          </Box>
          
          <Heading size="md">{apartment_name}</Heading>
          <Text>${price}/month</Text>
          <Link href={url} isExternal>
            Apartment Website
            <ExternalLinkIcon mx='2px' />
          </Link>
          <Box d="flex" alignItems="center"> 
            <Button mt={2} colorScheme="blue" size="sm" onClick={onOpen}>View Details</Button>
            <Button 
              mt={2} 
              colorScheme="green" 
              size="sm" 
              ml={2}
              onClick={(e) => {
                if (user) {
                  onOpen2()
                } else {
                  toast({
                    title: 'Please login first',
                    description: "You must be logged in to do that.",
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                  })
                }
              }}
            >
              Email Tenant
            </Button>
          </Box>
        </Box>
      </Box>



      <Modal isOpen={isOpen} onClose={onClose} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Viewing Poster's Message</ModalHeader>
          <ModalBody>
            {details}
          </ModalBody>

          <ModalFooter>
            <Button colorScheme='blue' mr={3} onClick={onClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      <Modal isOpen={isOpen2} onClose={onClose2} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Send an Email to Poster</ModalHeader>
          <ModalBody>
            <Textarea onChange={(e) => setContent(e.target.value)}>

            </Textarea>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme='green' mr={3} onClick={(e) => {
              
                const sendEmail = async () => {
                  try {
                    await axios.post(`http://localhost:8000/api/email_tenant?tenant_username=${username}&subtenant_username=${user.user_name}&email_text=${content}&apartment_slug=${apartment_slug}`)
                    onClose2()
                    toast({
                      title: 'Email sent!',
                      description: "An email has been sent to the poster.",
                      status: 'success',
                      duration: 9000,
                      isClosable: true,
                    })
                  } catch (e) {
                    console.log(e)
                  }
                }
                sendEmail()
              } 
            
            }>
              Send Email
            </Button>
            <Button colorScheme='blue' mr={3} onClick={onClose2}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>


    </Box>
  )
}

export default Sublease