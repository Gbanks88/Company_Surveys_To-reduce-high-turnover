import React, { useState, useEffect } from 'react';
import {
  ChakraProvider,
  Box,
  VStack,
  Grid,
  theme,
  Container,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from '@chakra-ui/react';
import RequirementsTable from './components/RequirementsTable';
import UseCasesTable from './components/UseCasesTable';
import RequirementForm from './components/RequirementForm';
import UseCaseForm from './components/UseCaseForm';
import TraceabilityMatrix from './components/TraceabilityMatrix';

function App() {
  const [requirements, setRequirements] = useState([]);
  const [useCases, setUseCases] = useState([]);

  useEffect(() => {
    fetchRequirements();
    fetchUseCases();
  }, []);

  const fetchRequirements = async () => {
    try {
      const response = await fetch('http://localhost:8000/requirements/');
      const data = await response.json();
      setRequirements(data.requirements);
    } catch (error) {
      console.error('Error fetching requirements:', error);
    }
  };

  const fetchUseCases = async () => {
    try {
      const response = await fetch('http://localhost:8000/use-cases/');
      const data = await response.json();
      setUseCases(data.use_cases);
    } catch (error) {
      console.error('Error fetching use cases:', error);
    }
  };

  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={3}>
          <Container maxW="container.xl">
            <VStack spacing={8}>
              <Tabs isFitted variant="enclosed" width="100%">
                <TabList mb="1em">
                  <Tab>Requirements</Tab>
                  <Tab>Use Cases</Tab>
                  <Tab>Traceability</Tab>
                  <Tab>Create Requirement</Tab>
                  <Tab>Create Use Case</Tab>
                </TabList>
                <TabPanels>
                  <TabPanel>
                    <RequirementsTable 
                      requirements={requirements}
                      onUpdate={fetchRequirements}
                    />
                  </TabPanel>
                  <TabPanel>
                    <UseCasesTable 
                      useCases={useCases}
                      onUpdate={fetchUseCases}
                    />
                  </TabPanel>
                  <TabPanel>
                    <TraceabilityMatrix 
                      requirements={requirements}
                      useCases={useCases}
                    />
                  </TabPanel>
                  <TabPanel>
                    <RequirementForm onSubmit={fetchRequirements} />
                  </TabPanel>
                  <TabPanel>
                    <UseCaseForm 
                      onSubmit={fetchUseCases}
                      requirements={requirements}
                    />
                  </TabPanel>
                </TabPanels>
              </Tabs>
            </VStack>
          </Container>
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default App;
