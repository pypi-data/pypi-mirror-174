# PHAT

the *Physical Hardware Authentication Tool*

---

### What it does

PHAT is a 2FA/MFA program designed to utilize external drives in a way that allows third-party programs to store isolated encryption keys on them. This gives the user the experience of using a [Hardware Key](https://en.wikipedia.org/wiki/Security_token), just with a normal USB.  

To do this, PHAT creates a simple folder (called $PHAT) containing user information in a decrypted JSON file (note: this file currently only contains the user's name, nothing confidential) along with an encrypted database containing the generated program keys.  

Each generated key is completely different and cannot be used to decrypt anything encrypted with another key; however, they are stored in `Program Name: Raw Key` format, meaning key names could be spoofed (protections against this are a WIP).


### Installation

⚠️ **WARNING: This is alpha software, do NOT use it for important or otherwise confidential data.**

PHAT can be installed either via PyPI or via Github directly (**recommended**). It is worth nothing that if a security update is released, PyPI will receive it **after** Github does. You can install either version like so:
```sh
python3 -m pip install phat2fa  # PyPI release
python3 -m pip install git+https://github.com/iiPythonx/phat  # Development
```  

After installation, run `phatsetup` in your terminal and follow the setup wizard.  
You can now use/create programs that utilize the PHAT authentication API.


### Roadmap

- [x] Simple 2FA key storage
- [ ] Single-machine encryption
- [ ] Third-party signature verification (to prevent program spoofing)
- [ ] PHAT client verification (to prevent people stealing passwords)


### Credits

Thanks to [DmmD](https://github.com/Dm123321_31mD) and [Emy](https://github.com/Commutxr) for bug testing PHAT before going public on Github.

### License

PHAT is under the MIT license, more information [here](https://opensource.org/licenses/MIT).  
LICENSE.txt contains the raw license.