from rdkit import Chem

from grongier.pex import BusinessProcess

from msg import (GenerateSdfRequest, GenerateSdfResponse, 
                SmilesRequest, SmilesResponse, 
                CompareRequest, CompareResponse,
                SdfExtractorRequest, SdfExtractorResponse,
                CreateSdfRequest, CreateSdfResponse,
                PkaRequest,CreateImageRequest)

class GenerateSdFileProcess(BusinessProcess):
    """
    Generate the sdf file
    """
    def on_message(self, request:GenerateSdfRequest) -> GenerateSdfResponse:
        """

        """
        rsp = self.send_request_sync("Python.bordkit.RDKitOperation", SmilesRequest(smiles=request.smiles))

        create_sdfile = self.send_request_sync("Python.bosdf.SdfOperation", CreateSdfRequest(properties=rsp.properties, filename=request.filename))
        
        return GenerateSdfResponse(
            filename=create_sdfile.filename
        )

class SmilesProcess(BusinessProcess):
    """
    Main process to get the properties from the smiles
    """
    def on_message(self, request:SmilesRequest) -> SmilesResponse:
        """
        Main function to get the properties from the smiles
        """
        rsp = SmilesResponse()
        rsp.smiles = request.smiles

        rsp_rdkit = self.send_request_sync("Python.bordkit.RDKitOperation", SmilesRequest(smiles=request.smiles))
        rsp.properties = rsp_rdkit.properties

        rsp_iupa = self.send_request_sync("Python.bomisc.IUPACOperation", SmilesRequest(smiles=request.smiles))
        rsp.properties.iupac_name = rsp_iupa.properties.iupac_name

        pka_rsp = self.send_request_sync("Python.bopka.PkaPredictorOperation", PkaRequest(smiles=request.smiles))

        rsp.properties.pka = pka_rsp.pka
        rsp.properties.pka_type = pka_rsp.pka_type

        self.send_request_sync("Python.bomisc.GenerateImageOperation", CreateImageRequest(smiles=request.smiles, filename="image.png"))

        return rsp

class CompareProcess(BusinessProcess):
    """

    """
    def on_message(self, request:CompareRequest) -> CompareResponse:
        """

        """
        # get the properties from the sdf file
        prop_sdf = self.extract_sdf_properties(request.filename)
        # get the properties from the smiles
        prop_smiles = self.extract_smiles_properties(request.smiles)
        # diff the properties
        diff_prop = self.diff_properties(prop_smiles, prop_sdf)

        return CompareResponse(
            prop_smiles=prop_smiles,
            prop_sdf=prop_sdf,
            diff_prop=diff_prop
        )

    def diff_properties(self, prop_smiles, prop_sdf):
        """
        Diff the properties
        """
        # diff the properties name and value
        diff_prop = {k: (v, prop_sdf[k]) for k, v in prop_smiles.items() if k in prop_sdf and v != prop_sdf[k]}
        # diff the properties name
        diff_prop_name = {k: (v, prop_sdf[k]) for k, v in prop_smiles.items() if k not in prop_sdf}
        diff_prop_name.update({k: (v, prop_sdf[k]) for k, v in prop_sdf.items() if k not in prop_smiles})
        # add the diff properties name
        diff_prop.update(diff_prop_name)

        return diff_prop

    def extract_smiles_properties(self, smiles):
        """
        Extract the properties from the smiles
        """
        msg = SmilesRequest(smiles=smiles)
        rsp = self.send_request_sync("Python.bp.SmilesProcess", msg)

        properties = rsp.properties.__dict__
        # change all the properties name in lower case
        properties = {k.lower(): v for k, v in properties.items()}

        return properties

    def extract_sdf_properties(self,filename):
        """
        Extract the properties from the sdf file
        """
        msg = SdfExtractorRequest(filename=filename)
        rsp = self.send_request_sync("Python.bosdf.SdfOperation", msg)

        return rsp.properties.__dict__

if __name__ == "__main__":
    # create the process
    process = CompareProcess()
    # start the process
    filename = '/Users/grongier/git/iris-chemicals-properties/misc/test.sdf'
    msg = CompareRequest(filename=filename, smiles="CC(=O)Nc1ccc(cc1)C(=O)O")
    rsp = process.on_message(msg)
    # print the result
    print(rsp)
    # process = GenerateSdFileProcess()
    # msg = GenerateSdfRequest(smiles="CC(=O)Nc1ccc(cc1)C(=O)O", filename="/Users/grongier/git/iris-chemicals-properties/misc/test.sdf")
    # process.on_message(msg)