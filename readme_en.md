# Installation

## Using pip

1. Run the following command in your terminal:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Copy the example configuration file:

   ```bash
   cp config.example.yaml config.yml
   ```

---

# If the Indonesian TTS Voice Is Not Available on Windows

## How to Add Indonesian Language and Enable TTS Voice

1. Open **Settings** > **Time & Language** > **Language & Region**
2. Click **Add a language**, then search for and add **Indonesian**
3. After adding the language, go to **Speech** settings
4. Click **Add voices**
5. Find and select **Indonesian**, then click **Install**
6. Once the installation is complete, locate the file `clone_voices.ps1`
7. **To run `clone_voices.ps1` as Administrator:**

   * Click **Start**, type **PowerShell**
   * Right-click **Windows PowerShell** or **Windows Terminal** and select **Run as administrator**
   * Navigate to the folder where `clone_voices.ps1` is located:

     ```powershell
     cd "C:\path\to\folder"
     ```
   * Run the script by typing:

     ```powershell
     .\clone_voices.ps1
     ```

---

## Running the script with Execution Policy Bypass

If you get an error saying script execution is disabled, you can run the script temporarily bypassing the policy by running this command **in a normal PowerShell window**:

```powershell
powershell -ExecutionPolicy Bypass -File .\clone_voices.ps1
```

---

For further questions or assistance, please visit:
[https://github.com/NotYusta](https://github.com/NotYusta)


