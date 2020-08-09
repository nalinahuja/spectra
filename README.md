# Spectra

<p align="justify">
Spectra is an image processing algorithm able to detect scenes, similarity, and blur in time ordered ordered image databases. The algorithm is capable of categorizing images based on scenes and give suggestions to the user to review and delete similar and or blurry image files.<br><br>Spectra does not mine or upload user data in any way and operates completely offline. It should be noted that a .spectra_data file and .spectra_temp folder are generated in every directory analyzed in order to speed up the analysis of that directory in the future.<br><br>Supports JPG, JPEG, PNG, and TIFF file formats.
</p>

## Compatibility

<p align="justify">
Spectra is officially compatible with macOS and popular Linux distributions.
</p>

## Dependencies

<p align="justify">
Spectra requires several dependencies to operate as a command line utility. You must have the latest version of <code>python3</code> and <code>pip3</code> installed on your computer to use the program. You will also need to install the latest <code>python3</code> packages of PIL, shutil, cv2, imagehash, numpy, scipy, skimage, and sklearn. These packages should be setup automatically by the installation script that is included with this repository, so its not necessary to install all of them all on your own.
</p>

## Installation

<p align="justify">
Please navigate to the <a href="https://github.com/nalinahuja22/spectra/releases">release</a> tab of this repository and download the latest version of this project. You can perform this download within a browser environment or using a command line utility like <code>wget</code> or <code>curl</code>. Alternatively, you can clone this <a href="https://github.com/nalinahuja22/spectra">repository</a> but it is recommended that you download the most recent release as the git repository is comparatively larger.
</p>

<p align="justify">
Then, navigate to the location where the Spectra repository contents have been downloaded onto your machine and run the <a href="https://github.com/nalinahuja22/spectra/blob/master/install_spectra">install_spectra</a> script. This executable will install Spectra to your home directory as a hidden folder called <code>~/.spectra</code> and install all the dependencies required by Spectra, assuming that you have <code>python3</code> and <code>pip3</code> installed on your machine. When the installation script finishes, restart your terminal and source your terminal profile to fully configure the installation.<br><br>If you would like to do a manual installation of Spectra, all you need to do is move the repository contents you downloaded into a folder at <code>~/.spectra</code> which you will have to create yourself. Then add the following function to your terminal profile. Then simply source your terminal profile and Spectra should be setup.
</p>

```
spectra() {
  command python3 ~/.spectra/bin/spectra.py $@
}
```

## Usage

<p align="justify">
Spectra takes up to four input values, only one of which is required. The image path is required to run the script and must always be the first argument passed to Spectra. The sensitivity flags on the other hand, are optional, and can be indicated in any order to Spectra. It is not necessary to indicate the sensitivity thresholds since there are default values for them internally that work for most image data sets. However, if you need to indicate a sensitivity threshold, you simpily indicate the flag and then the sensitivity expressed as a percentage from 0 to 100, where 100 percent results in the most sensitive image processing and vice versa.
</p>

```
spectra [IMAGE_PATH] [-b BLUR_SENSITIVITY] [-s SCENE_SENSITIVITY] [-d DUPLICATE_SENSITIVITY]
```
