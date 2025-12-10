> [!IMPORTANT]
> The dataset "SONY_IMX135" produced by [INTEL-TAU](https://arxiv.org/abs/1910.10404) is not included in the repository due to its size of 2.33 GB. It is avaliable to download [here](https://download.fairdata.fi:443/download?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NjU1MDM0NjYsImRhdGFzZXQiOiJmMDU3MGEzZi0zZDc3LTRmNDQtOWVmMS05OWFiNDg3OGYxN2MiLCJmaWxlIjoiL1NvbnlfSU1YMTM1LnppcCIsInByb2plY3QiOiIyMDAwNDY0IiwicmFuZG9tX3NhbHQiOiI3Yzc0ZDU5OCJ9.j_xNXfEMoCS7HQ_SUoMpMiqIeOrt2JBW1KS_jqtHPYk).

<h1 align="center">Spatially-Adaptive Log-Chroma White Balance</h1>

*A Spatially-Adaptive Log-Chroma White Balance (SALC-WB) algorithm on raw images.  Traditional methods, such as Gray World and Shades-of-Gray, compute global statistical estimations that often fail in locally varied lighting. This pipeline combines local statistical estimation in log-chroma space with a Shades-of-Gray prior. Unlike existing methods that require training or complex optimizations, is a simple and efficient AWB algorithm that recovers accurate luminance and reduces local artifacts.*

## How to run

1. Clone the repository
```
git clone https://github.com/akrossu/salc-wb.git
cd salc-wb
```

2. [Download](https://download.fairdata.fi/download?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NjU1MDM0NjYsImRhdGFzZXQiOiJmMDU3MGEzZi0zZDc3LTRmNDQtOWVmMS05OWFiNDg3OGYxN2MiLCJmaWxlIjoiL1NvbnlfSU1YMTM1LnppcCIsInByb2plY3QiOiIyMDAwNDY0IiwicmFuZG9tX3NhbHQiOiI3Yzc0ZDU5OCJ9.j_xNXfEMoCS7HQ_SUoMpMiqIeOrt2JBW1KS_jqtHPYk) and Extract the contents of the Sony_IMX135 folder into the root folder of the project
```
.
├── Sony_IMX135/
|   ├── field_3_cameras/
|   ├── lab_printouts/
|   └── lab_realscene
├── lib/
├── Paper/
├── Presentation/
├── README.md
├── requirements.txt
├── salc-wb.py
└── tests.py
```

4. Create a [virtual python environment](https://docs.python.org/3/library/venv.html)

5. Install the required libraries using `pip install -r requirements.txt`

6. Run `salc-wb.py`
> Note: debug is default enabled, but can be set to false
