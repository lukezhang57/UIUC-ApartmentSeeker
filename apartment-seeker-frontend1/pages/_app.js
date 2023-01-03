import { ChakraProvider } from '@chakra-ui/react'
import { extendTheme } from "@chakra-ui/react";

const extendedTheme = extendTheme({

  styles: {
    global: (props) => ({
      body: {
        bg: '#F7FAFC'
      }
    })
  },
})


function MyApp({ Component, pageProps }) {
  return (
    <ChakraProvider theme={extendedTheme}>
      <Component {...pageProps} />
    </ChakraProvider>
  )
}

export default MyApp
