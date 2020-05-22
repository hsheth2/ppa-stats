from fastapi import FastAPI
import app.stats as stats
from typing import List, Dict, Any

app = FastAPI()

@app.get('/api/owner/{ppa_owner}/ppa/{ppa_name}/package/{package_name}/downloads')
def downloads(ppa_owner: str, ppa_name: str, package_name: str) -> List[Dict[str, Any]]:
    binaries = stats.get_binaries(ppa_owner, ppa_name, package_name)

    downloads = []
    for binary in binaries:
        info = stats.get_binary_info(binary)
        downloads.append(info)
    return downloads


@app.get('/api/owner/{ppa_owner}/list_ppas')
def list_ppas(ppa_owner: str) -> List[str]:
    lp = stats.launchpad
    owner = lp.people[ppa_owner]
    
    ppas = []
    for ppa in owner.ppas:
        ppas.append(ppa.name)
    return ppas

@app.get('/api/owner/{ppa_owner}/ppa/{ppa_name}/list_packages')
def list_packages(ppa_owner: str, ppa_name: str) -> List[str]:
    lp = stats.launchpad
    owner = lp.people[ppa_owner]
    ppa = owner.getPPAByName(name=ppa_name)

    packages = set()
    for binary in ppa.getPublishedBinaries(status="Published"):
        package = binary.binary_package_name
        packages.add(package)
    return list(packages)
