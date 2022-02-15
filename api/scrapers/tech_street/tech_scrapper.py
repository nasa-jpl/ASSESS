import json
import os
from tqdm import tqdm

from utils import get_sdo_urls, get_category_urls, extract_hierarchy, get_standards_list, get_standard_details

out_dir='data'
all_SDOs_url = "https://www.techstreet.com/publishers/list"

def scrape_SDO(SDO_url, SDO_name, fresh=False, semi_fresh=False):
    """
    :param SDO_url:
    :param SDO_name:
    :return: 1. fetches and extracts the hierarchy of categories and their standards and saves it into a hierarchy_<SDO_suffix/abbrev>.json file
            2. fetches and extracts the standards from above, extracts the metadata into a json and saves it into a standards_metadta_<SDO_suffix/abbrev>.json file.
    Important Note:- If a page was previously fetched, we do not fetch it again, we use a cached version from data/http-cache
    """
    # get the top level categories in the SDO
    sdo_suffix = SDO_url.replace('https://www.techstreet.com/publishers/', '')
    cat_urls = get_category_urls(SDO_url, fresh=fresh or semi_fresh)
    print('category urls:', cat_urls)

    # get the categorical hierarchy from the site, any of the above extracted tlc links could be used here as all of them take you to the same page!
    categorical_hierarchy = extract_hierarchy(cat_urls[0]['link'], fresh=fresh or semi_fresh)
    hierarchy={'SDO_name':SDO_name, 'SDO_url': SDO_url, 'categorical_hierarchy': categorical_hierarchy}
    # print('hierarchy:', hierarchy)

    # add standards links to the hierarchy and save as json
    for cat, cat_info in categorical_hierarchy.items():
        if cat_info['url'] != '':
            print('Getting standards for category:', cat, '(' + cat_info['url'] + ')')
            standards_list = get_standards_list(cat_info['url'], fresh=fresh or semi_fresh)
            categorical_hierarchy[cat]['standards'] = standards_list
    hierarchy_file = open(os.path.join(out_dir, 'hierarchy_' + sdo_suffix + '.json'), 'w')
    hierarchy_file.write(json.dumps(hierarchy, indent=2))
    hierarchy_file.close()

    # fetch the standards pages and extract relevant info
    hierarchy_file = open(os.path.join(out_dir, 'hierarchy_' + sdo_suffix + '.json'), 'r').read()
    hierarchy = json.loads(hierarchy_file)
    all_sdo_standards = [cat_info['standards'] for cat, cat_info in hierarchy['categorical_hierarchy'].items() if
                         cat_info['url'] != '' and 'standards' in cat_info.keys()]
    all_sdo_standards = set(
        [item for sublist in all_sdo_standards for item in sublist])  # flatten and deduplicate the list of lists

    print('Num of Standards to extract:', len(all_sdo_standards))
    standards_metadata = {}
    for standard_link in tqdm(all_sdo_standards):
        metadata = get_standard_details(standard_link, fresh=fresh)
        standards_metadata[standard_link] = metadata

    standards_metadata_file = open(os.path.join(out_dir, 'standards_metadata_' + sdo_suffix + '.json'), 'w')
    standards_metadata_file.write(json.dumps(standards_metadata, indent=2))
    standards_metadata_file.close()


if __name__ == "__main__":

    get_SDO_list=False
    if get_SDO_list:
        # get the names and links to the SDOs available in the website
        SDO_list = get_sdo_urls(all_SDOs_url)
        for SDO_info in SDO_list:
            SDO_name=SDO_info['name']
            SDO_url = SDO_info['sdo_url']
            print(SDO_url, SDO_name)
list=[
"https://www.techstreet.com/publishers/asnt ASNT - American Society for Nondestructive Testing",
"https://www.techstreet.com/publishers/asq ASQ - American Society for Quality",
# "https://www.techstreet.com/publishers/asse (plumbing) ASSE (Plumbing) - American Society of Sanitary Engineering",
"https://www.techstreet.com/publishers/assp ASSP - American Society of Safety Professionals (Formerly ASSE)",
"https://www.techstreet.com/publishers/astm ASTM - ASTM International"
]

for item in list:
    item=item.split(" ", 1)
    link, name=item[0], item[1]
    print('fecthing link:', link)
    print('name:', link, name)
    scrape_SDO(link, name)

"""
Refs:
1. Getting Splash Running in your local: https://splash.readthedocs.io/en/stable/install.html#os-x-docker

Todo:
- what if there is not hierarchy on the page!
- add a flag in the funcitons so that fresh sdo standards are fetched
- add a function which only updates/replaces the ES data for a particular SDO
- make sure that the status historical/latest is calculated based on published date before ES ingestion

All SDO list:
https://www.techstreet.com/publishers/3a 3A - 3-A Sanitary Standards
https://www.techstreet.com/publishers/285054 9000 - 9000 Store
https://www.techstreet.com/publishers/aa AA - Aluminum Association
https://www.techstreet.com/publishers/aama AAMA - American Architectural Manufacturers Association
https://www.techstreet.com/publishers/aami AAMI - Association for the Advancement of Medical Instrumentation
https://www.techstreet.com/publishers/aashto AASHTO - American Association of State and Highway Transportation Officials
https://www.techstreet.com/publishers/aatcc AATCC - American Association of Textile Chemists and Colorists
https://www.techstreet.com/publishers/abcb ABCB - Australian Building Codes Board
https://www.techstreet.com/publishers/abma ABMA - American Bearing Manufacturers Association
https://www.techstreet.com/publishers/abma-boiler ABMA-Boiler - American Boiler Manufacturers Association
https://www.techstreet.com/publishers/acc ACC - American Chemistry Council
https://www.techstreet.com/publishers/acgih ACGIH - American Conference of Governmental Industrial Hygienists
https://www.techstreet.com/publishers/aci ACI - American Concrete Institute
https://www.techstreet.com/publishers/ada ADA - American Dental Association
https://www.techstreet.com/publishers/ads ADS - SAE ITC TSC Aerospace Standards (Formerly ADS Group Limited)
https://www.techstreet.com/publishers/aeic AEIC - Association of Edison Illuminating Companies
https://www.techstreet.com/publishers/aga AGA - American Gas Association
https://www.techstreet.com/publishers/aham AHAM - Association of Home Appliance Manufacturers
https://www.techstreet.com/publishers/ahp AHP - American Herbal Pharmacopoeia
https://www.techstreet.com/publishers/ahri AHRI - Air-Conditioning, Heating, and Refrigeration Institute (formerly ARI)
https://www.techstreet.com/publishers/aia AIA - Aerospace Industries Association
https://www.techstreet.com/publishers/aiaa AIAA - American Institute of Aeronautics and Astronautics
https://www.techstreet.com/publishers/aisc AISC - American Institute of Steel Construction
https://www.techstreet.com/publishers/ali ALI - American Ladder Institute
https://www.techstreet.com/publishers/amca AMCA - Air Movement and Control Association
https://www.techstreet.com/publishers/ans ANS - American Nuclear Society
https://www.techstreet.com/publishers/ansi ANSI - American National Standards Institute
https://www.techstreet.com/publishers/287754 ANSI/ANSLG - American National Standards Institute / American National Standard Lighting Group
https://www.techstreet.com/publishers/287756 ANSI/NEMA - American National Standards Institute / National Electrical Manufacturers Association
https://www.techstreet.com/publishers/289074 ANSI/TCNA - Tile Council of North America, Inc.
https://www.techstreet.com/publishers/api API - American Petroleum Institute
https://www.techstreet.com/publishers/apwa APWA - American Public Works Association
https://www.techstreet.com/publishers/as AS - Standards Australia
https://www.techstreet.com/publishers/asa ASA - American National Standards of the Acoustical Society of America
https://www.techstreet.com/publishers/31 ASAE/ASABE - The American Society of Agricultural and Biological Engineers
https://www.techstreet.com/publishers/asce ASCE - American Society of Civil Engineers
https://www.techstreet.com/publishers/asd-stan pren ASD-STAN prEN - ASD-STAN Standardization
https://www.techstreet.com/publishers/ashe ASHE - American Society for Healthcare Engineering
-- (incomplete) https://www.techstreet.com/publishers/ashrae ASHRAE - ASHRAE
https://www.techstreet.com/publishers/asis ASIS - ASIS International
https://www.techstreet.com/publishers/asm ASM - ASM International
https://www.techstreet.com/publishers/asme ASME - ASME International
https://www.techstreet.com/publishers/asnt ASNT - American Society for Nondestructive Testing
https://www.techstreet.com/publishers/asq ASQ - American Society for Quality
-- (the url is weird) https://www.techstreet.com/publishers/asse (plumbing) ASSE (Plumbing) - American Society of Sanitary Engineering
https://www.techstreet.com/publishers/assp ASSP - American Society of Safety Professionals (Formerly ASSE)
https://www.techstreet.com/publishers/astm ASTM - ASTM International

https://www.techstreet.com/publishers/atis ATIS - The Alliance for Telecommunications Industry Solutions
https://www.techstreet.com/publishers/awc AWC - American Wood Council
https://www.techstreet.com/publishers/awi AWI - Architectural Woodwork Institute
https://www.techstreet.com/publishers/awpa AWPA - American Wood Protection Association
https://www.techstreet.com/publishers/aws AWS - American Welding Society
https://www.techstreet.com/publishers/awwa AWWA - American Water Works Association
https://www.techstreet.com/publishers/b11 B11 - B11 Standards, Inc.
https://www.techstreet.com/publishers/bhma BHMA - Builders Hardware Manufacturers Association
https://www.techstreet.com/publishers/bicsi BICSI - BICSI, A Telecommunications Association
https://www.techstreet.com/publishers/bifma BIFMA - Business and Institutional Furniture Manufacturers Association
https://www.techstreet.com/publishers/boma BOMA - Building Owners and Managers Association International
https://www.techstreet.com/publishers/bs BS - BSI Group
https://www.techstreet.com/publishers/bv BV - Bureau Veritas Consumer Product Services, Inc.
https://www.techstreet.com/publishers/bioworld BioWorld - Thomson Reuters BioWorld
https://www.techstreet.com/publishers/285034 CAN/CGSB - Canadian General Standards Board
https://www.techstreet.com/publishers/285754 CAN/ULC - Underwriters Laboratories of Canada
https://www.techstreet.com/publishers/cfr CFR - Code of Federal Regulations
https://www.techstreet.com/publishers/cga CGA - Compressed Gas Association
https://www.techstreet.com/publishers/cgsb CGSB - Canadian General Standards Board
https://www.techstreet.com/publishers/cie CIE - Commission Internationale de L'Eclairage
https://www.techstreet.com/publishers/cii CII - Construction Industry Institute
https://www.techstreet.com/publishers/cirs CIRS - Centre for Innovation in Regulatory Science
https://www.techstreet.com/publishers/cispr CISPR - International Special Committee on Radio Interference
https://www.techstreet.com/publishers/clsi CLSI - Clinical and Laboratory Standards Institute
https://www.techstreet.com/publishers/cmaa CMAA - Crane Manufacturers Association of America
https://www.techstreet.com/publishers/cmr CMR - CMR International
https://www.techstreet.com/publishers/crsi CRSI - Concrete Reinforcing Steel Institute
https://www.techstreet.com/publishers/csa CSA - CSA Group
https://www.techstreet.com/publishers/cta CTA - Consumer Technology Association (Formerly CEA)
https://www.techstreet.com/publishers/cti CTI - Cooling Technology Institute
https://www.techstreet.com/publishers/did DID - Data Item Description
https://www.techstreet.com/publishers/din DIN - Deutsches Institut Fur Normung E.V. (German National Standard)
https://www.techstreet.com/publishers/dod DOD - Department of Defense
https://www.techstreet.com/publishers/doxpub DOXPUB - Doxpub, Inc.
https://www.techstreet.com/publishers/eec EEC - European Union Directives
https://www.techstreet.com/publishers/eemua EEMUA - Engineering Equipment and Materials Users Association
https://www.techstreet.com/publishers/esd ESD - EOS/ESD Association, Inc.
https://www.techstreet.com/publishers/etsi ETSI - European Telecommunications Standards Institute
https://www.techstreet.com/publishers/fci FCI - Fluid Controls Institute
https://www.techstreet.com/publishers/fed FED - Federal Specifications and Standards
https://www.techstreet.com/publishers/fm approvals FM Approvals - FM Approvals
https://www.techstreet.com/publishers/frpi FRPI - Fiberglass Reinforced Plastics Institute, Inc.
https://www.techstreet.com/publishers/gpa GPA - GPA Midstream Association
https://www.techstreet.com/publishers/hei HEI - Heat Exchange Institute
https://www.techstreet.com/publishers/hfes HFES - Human Factors and Ergonomics Society
https://www.techstreet.com/publishers/hi HI - Hydraulic Institute
https://www.techstreet.com/publishers/hir HIR - H.I.R. Technical Services
https://www.techstreet.com/publishers/i3a I3A - International Imaging Industry Association
https://www.techstreet.com/publishers/iadc IADC - International Association of Drilling Contractors
https://www.techstreet.com/publishers/iapmo IAPMO - International Association of Plumbing and Mechanical Officials
https://www.techstreet.com/publishers/iata IATA - International Air Transport Association
https://www.techstreet.com/publishers/icao ICAO - International Civil Aviation Organization
https://www.techstreet.com/publishers/icc ICC - International Code Council
https://www.techstreet.com/publishers/icea ICEA - Insulated Cable Engineers Association
https://www.techstreet.com/publishers/icml ICML - International Council for Machinery Lubrication
https://www.techstreet.com/publishers/iec IEC - International Electrotechnical Commission
https://www.techstreet.com/publishers/ieee IEEE - IEEE
https://www.techstreet.com/publishers/ies IES - Illuminating Engineering Society
https://www.techstreet.com/publishers/iest IEST - Institute of Environmental Sciences and Technology
https://www.techstreet.com/publishers/ifi IFI - Industrial Fasteners Institute
https://www.techstreet.com/publishers/iicrc IICRC - The Institute of Inspection, Cleaning, and Restoration Certification
https://www.techstreet.com/publishers/incits INCITS - InterNational Committee for Information Technology Standards (formerly NCITS)
https://www.techstreet.com/publishers/ipc IPC - Association Connecting Electronics Industries
https://www.techstreet.com/publishers/isa ISA - The International Society of Automation
https://www.techstreet.com/publishers/isea ISEA - International Safety Equipment Association
https://www.techstreet.com/publishers/iso ISO - International Organization for Standardization
https://www.techstreet.com/publishers/ispe ISPE - International Society for Pharmaceutical Engineering
https://www.techstreet.com/publishers/ista ISTA - International Safe Transit Association
https://www.techstreet.com/publishers/jedec JEDEC - JEDEC Solid State Technology Association
https://www.techstreet.com/publishers/jis JIS - Japanese Industrial Standard / Japanese Standards Association
https://www.techstreet.com/publishers/lia LIA - Laser Institute of America
https://www.techstreet.com/publishers/mbma MBMA - Metal Building Manufacturers Association
https://www.techstreet.com/publishers/mil MIL - Military Specifications and Standards
https://www.techstreet.com/publishers/mmpds MMPDS - Metallic Materials Properties Development and Standardization
https://www.techstreet.com/publishers/mpif MPIF - Metal Powder Industries Federation
https://www.techstreet.com/publishers/mss MSS - Manufacturers Standardization Society
https://www.techstreet.com/publishers/naamm NAAMM - National Association of Architectural Metal Manufacturers
https://www.techstreet.com/publishers/nace NACE - National Association of Corrosion Engineers
https://www.techstreet.com/publishers/nadca NADCA - National Air Duct Cleaners Association
https://www.techstreet.com/publishers/nas NAS - Aerospace Industries Association - National Aerospace Standard
https://www.techstreet.com/publishers/nasa NASA - National Aeronautics and Space Administration
https://www.techstreet.com/publishers/nbbi NBBI - National Board of Boiler and Pressure Vessel Inspectors
https://www.techstreet.com/publishers/ncsl NCSL - National Conference of Standards Laboratories International
https://www.techstreet.com/publishers/neca NECA - National Electrical Contractors Association
https://www.techstreet.com/publishers/nema NEMA - National Electrical Manufacturers Association
https://www.techstreet.com/publishers/neta NETA - International Electrical Testing Association
https://www.techstreet.com/publishers/nfpa (fire) NFPA (Fire) - National Fire Protection Association
https://www.techstreet.com/publishers/nfpa (fluid) NFPA (Fluid) - National Fluid Power Association
https://www.techstreet.com/publishers/nfsi NFSI - National Floor Safety Institute
https://www.techstreet.com/publishers/nga NGA - National Glass Association
https://www.techstreet.com/publishers/niso NISO - National Information Standards Organization
https://www.techstreet.com/publishers/norsok NORSOK - NORSOK
https://www.techstreet.com/publishers/nrc NRC - National Research Council Canada
https://www.techstreet.com/publishers/nsc NSC - Natural Stone Council
https://www.techstreet.com/publishers/nsf NSF - NSF International
https://www.techstreet.com/publishers/nzs NZS - Standards New Zealand
https://www.techstreet.com/publishers/opei OPEI - Outdoor Power Equipment Institute
https://www.techstreet.com/publishers/pci PCI - Precast/Prestressed Concrete Institute
https://www.techstreet.com/publishers/pda PDA - Parenteral Drug Association
https://www.techstreet.com/publishers/pei PEI - Petroleum Equipment Institute
https://www.techstreet.com/publishers/pip PIP - Process Industry Practices
https://www.techstreet.com/publishers/ppi PPI - Plastics Pipe Institute
https://www.techstreet.com/publishers/rtca RTCA - Radio Technical Commission for Aeronautics
https://www.techstreet.com/publishers/sae SAE - SAE International
https://www.techstreet.com/publishers/saia SAIA - Scaffold and Access Industry Association
https://www.techstreet.com/publishers/scte SCTE - Society of Cable Telecommunication Engineers
https://www.techstreet.com/publishers/sdi SDI - Steel Door Institute
https://www.techstreet.com/publishers/sept SEPT - Software Engineering Process Technology
https://www.techstreet.com/publishers/ses SES - The Society for Standards Professionals
https://www.techstreet.com/publishers/sia SIA - Security Industry Association
https://www.techstreet.com/publishers/sji SJI - Steel Joist Institute
https://www.techstreet.com/publishers/smacna SMACNA - Sheet Metal and Air Conditioning Contractors' National Association
https://www.techstreet.com/publishers/sme SME - Society of Manufacturing Engineers
https://www.techstreet.com/publishers/smpte SMPTE - Society of Motion Picture and Television Engineers
https://www.techstreet.com/publishers/spc SPC - Standards Press of China
https://www.techstreet.com/publishers/spi SPI - Society of the Plastics Industry
https://www.techstreet.com/publishers/sspc SSPC - Society for Protective Coatings
https://www.techstreet.com/publishers/287461 STI/SPFA - Steel Tank Institute/Steel Plate Fabricators Association
https://www.techstreet.com/publishers/tappi TAPPI - Technical Association of the Pulp and Paper Industry
https://www.techstreet.com/publishers/tema TEMA - Tubular Exchanger Manufacturers Association
https://www.techstreet.com/publishers/tim TIM - Total Innovation Management (TIM) Foundation
https://www.techstreet.com/publishers/tms TMS - The Masonry Society
https://www.techstreet.com/publishers/uama UAMA - Unified Abrasives Manufacturers' Association
https://www.techstreet.com/publishers/ul UL - Underwriters Laboratories
https://www.techstreet.com/publishers/ulc ULC - Underwriters Laboratories of Canada
https://www.techstreet.com/publishers/uop UOP - UOP LLC, A Honeywell Company
https://www.techstreet.com/publishers/wrc WRC - Welding Research Council, Inc.
https://www.techstreet.com/publishers/x9 X9 - Accredited Standards Committee X9 Incorporated
"""
