#!/usr/bin/env bash

# Developed by Nalin Ahuja, nalinahuja22

# End Header---------------------------------------------------------------------------------------------------------------------------------------------------------

# Boolean Values
declare TRUE=1 FALSE=0

# Embedded Strings
declare YES="y"

# Program Path
declare SPECTRA_FOLD=~/.spectra

# Program Files
declare SPECTRA_BIN=./bin
declare SPECTRA_LICE=./LICENSE
declare SPECTRA_READ=./README.md

# Installation Resources
declare SPECTRA_LOG=./.installation_log

# Terminal Profiles
declare ZSHRC=~/.zshrc
declare BASHRC=~/.bashrc
declare BASHPR=~/.bash_profile

# End Defined Constants----------------------------------------------------------------------------------------------------------------------------------------------

declare install_status=${FALSE}

# End Global Variables-----------------------------------------------------------------------------------------------------------------------------------------------

# Prompt User For Confirmation
command read -p "Please confirm installation of Spectra [y/n]: " confirm

# Determine Action
if [[ "${confirm//Y/y}" == ${YES} ]]
then
  # Add Command To Terminal Profile
  if [[ ! -e ${SPECTRA_FOLD} ]]
  then
    # Find ~/.zshrc
    if [[ -f ${ZSHRC} ]]
    then
      # Add Command To .zshrc
      command echo -e "\n# Spectra Caller\n\nspectra() {\n  command python3 ~/.spectra/bin/spectra.py \"\$@\"\n}\n" >> ${ZSHRC} && install_status=${TRUE}
    fi

    # Find ~/.bashrc
    if [[ -f ${BASHRC} ]]
    then
      # Add Command To .bashrc
      command echo -e "\n# Spectra Caller\n\nspectra() {\n  command python3 ~/.spectra/bin/spectra.py \"\$@\"\n}\n" >> ${BASHRC} && install_status=${TRUE}
    fi

    # Find ~/.bash_profile
    if [[ -f ${BASHPR} ]]
    then
      # Add Command To .bash_profile
      command echo -e "\n# Spectra Caller\n\nspectra() {\n  command python3 ~/.spectra/bin/spectra.py \"\$@\"\n}\n" >> ${BASHPR} && install_status=${TRUE}
    fi

    # Check Command Installation Status
    if [[ ${install_status} == ${FALSE} ]]
    then
      # Display Error Prompt
      command echo -e "→ No bash configurations found, aborting Spectra installation"

      # Exit Installation
      command exit 1
    fi

    # Display Success Prompt
    command echo -e "→ Installed Spectra command to terminal configuration"
  fi

  # Install Spectra Program Files
  command mkdir ${SPECTRA_FOLD} 2> /dev/null
  command mv ${SPECTRA_BIN} ${SPECTRA_FOLD} 2> /dev/null
  command mv ${SPECTRA_LICE} ${SPECTRA_FOLD} 2> /dev/null
  command mv ${SPECTRA_READ} ${SPECTRA_FOLD} 2> /dev/null

  # Display Success Prompt
  command echo -e "→ Installed Spectra In ~/.spectra"

  # Install Python Dependency
  command echo -ne "→ Installing Python3 dependencies - 0%\r"
  command python3 -m pip install imagehash > ${SPECTRA_ERR}

  # Error Check Return
  if [[ ${?} -gt 0 ]]
  then
    command echo -e "Error: Python3 module (imagehash) could not be installed"
    command cat ${SPECTRA_ERR}
    command exit 1
  fi

  # Install Python Dependency
  command echo -ne "→ Installing Python3 Dependencies - 25%\r"
  command python3 -m pip install opencv-python > ${SPECTRA_ERR}

  # Error Check Return
  if [[ ${?} -gt 0 ]]
  then
    command echo -e "Error: Python3 module (opencv) could not be installed"
    command cat ${SPECTRA_ERR}
    command exit 1
  fi

  # Install Python Dependency
  command echo -ne "→ Installing Python3 Dependencies - 50%\r"
  command python3 -m pip install -U numpy scipy > ${SPECTRA_ERR}

  # Error Check Return
  if [[ ${?} -gt 0 ]]
  then
    command echo -e "Error: Python3 modules (numpy, scipy) could not be installed"
    command cat ${SPECTRA_ERR}
    command exit 1
  fi

  # Install Python Dependency
  command echo -ne "→ Installing Python3 Dependencies - 75%\r"
  command python3 -m pip install -U scikit-image scikit-learn > ${SPECTRA_ERR}

  # Error Check Return
  if [[ ${?} -gt 0 ]]
  then
    command echo -e "Error: Python3 modules (skimage, scikit-learn) could not be installed"
    command cat ${SPECTRA_ERR}
    command exit 1
  fi

  # Display Module Install Success
  command echo -ne "→ Installed Python3 dependencies       \r"

  # Display Installation Success Prompt
  command echo -e "\nSpectra successfully installed, please restart your terminal!"
else
  # Display Abort Prompt
  command echo -e "\nSpectra installation aborted"
fi
