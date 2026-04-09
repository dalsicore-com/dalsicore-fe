---
title: Create Biometric Authentication in Android | by Anaf Naufalian
excerpt: Biometric authentication has become increasingly popular in recent years as a secure and convenient way to authenticate user identities on mobile devices.
publishedAt: 2023-03-18
author: Anaf Naufalian
tags:
  - android
  - security
featured: false
draft: false
---

Create Biometric Authentication in Android | by Anaf Naufalian
==============================================================
[Anaf Naufalian](https://medium.com/@anafthdev_?source=post_page---byline--fbfbe77db7c6---------------------------------------)

Mar 18, 2023

![Photo by Lukenn Sabellano on Unsplash](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*qM8rnAt_7It11D-p)

Biometric authentication has become increasingly popular in recent years as a secure and convenient way to authenticate user identities on mobile devices. Android, the world’s most popular mobile operating system, has been quick to adopt biometric authentication technology, making it easier for users to access their devices securely.

Android supports various biometric authentication methods, including fingerprint recognition, face recognition, ect. These authentication methods are built into the operating system and can be used by developers to secure their applications.

Developers can also integrate biometric authentication into their applications, providing an additional layer of security. To do this, they can use Android’s BiometricPrompt API, which provides a standard interface for requesting biometric authentication from users. By using this API, developers can ensure that their applications are secure while also providing a seamless user experience.

Overall, biometric authentication on Android is a powerful and convenient way to secure user identities. With support for multiple biometric authentication methods and a developer-friendly API, Android makes it easy for users and developers alike to take advantage of this technology.

**Getting Started**

First, add the AndroidX Biometric dependency into **build.gradle** file:

```
dependencies {
    // Java language implementation
    implementation "androidx.biometric:biometric:1.1.0"
    // Kotlin
    implementation "androidx.biometric:biometric-ktx:1.2.0-alpha05"
}
```

> **Note:** to use biometric authentication, make sure the user has the features, such as fingerprint, facial recognition, etc.

**Check if the device supports biometrics**

Before implementing biometric authentication in an Android application, it is important to check whether the user’s device supports the biometric authentication method that the application intends to use. This is important to ensure that the user experience is seamless and that the application’s authentication system works as intended.

To check if the device supports biometric authentication, developers can call the `canAuthenticate()` method on the `BiometricManager` object, which is part of the AndroidX Biometric Library. This method returns a `BiometricManager.BIOMETRIC_SUCCESS` constant if the device supports biometric authentication, or one of several other constants if biometric authentication is not available for some reason (such as if the user has not enrolled any biometric data on the device).

for example, create a class named `BiometricHandler`:

```
class BiometricHandler(private val activity: FragmentActivity) {
 
    companion object {
        fun hasBiometric(context: Context, authenticators: Int = Authenticators.DEVICE_CREDENTIAL): Int {
           return BiometricManager.from(context).canAuthenticate(authenticators)
        }
    }
}
```

in the `canAuthenticate()` function we have to enter a value for the parameter named `authenticators`

parameter `authenticators`can be filled with:

*   **Authenticators._DEVICE_CREDENTIAL:_** The non-biometric credential used to secure the device (i.e. PIN, pattern, or password).
*   **Authenticators._BIOMETRIC_WEAK:_** indicates the use of a weaker biometric authentication method, such as fingerprint recognition, which is generally considered less secure compared to advanced methods like facial recognition or iris scanning.
*   **Authenticators.BIOMETRIC_STRONG:** indicates the use of advanced biometric authentication methods like facial recognition or iris scanning, which are more secure than fingerprint recognition.

Add a function below to ensure the device can use biometric prompt:

```
fun canAuthenticateWithAuthenticators(
    context: Context,
    authenticators: Int = Authenticators.DEVICE_CREDENTIAL
): Boolean {
    return hasBiometric(context, authenticators) == BiometricManager.BIOMETRIC_SUCCESS
}
```

**Create Prompt Info**

add this function into class `BiometricHandler`:

```
fun createPromptInfo(
    title: String,
    subtitle: String,
    description: String,
    negativeButtonText: String = "Cancel",
    allowedAuthenticators: Int = -1
): BiometricPrompt.PromptInfo {
    return BiometricPrompt.PromptInfo.Builder().apply {
        setTitle(title)
        setSubtitle(subtitle)
        setDescription(description)
   
        // allowedAuthenticators: DEVICE_CREDENTIAL or BIOMETRIC_WEAK or BIOMETRIC_STRONG
        if (allowedAuthenticators != -1) setAllowedAuthenticators(allowedAuthenticators)
        
        setNegativeButtonText(negativeButtonText)
    }.build()
}
```

The `BiometricPrompt.PromptInfo.Builder()` constructor creates a new instance of a `BiometricPrompt.PromptInfo.Builder` object that can be used to configure various options for the biometric prompt, such as the title, subtitle, description, allowed authenticators, and others.

By using the `BiometricPrompt.PromptInfo.Builder()` constructor and the builder methods, developers can create and customize biometric authentication prompts to provide a seamless and user-friendly experience for their users. Once the builder object is configured, it can be passed to the `BiometricPrompt` constructor to create a biometric authentication prompt.

`setAllowedAuthenticators()` method used for control the types of biometric authentication methods that are allowed for use in their applications. This can help to ensure that the authentication process is secure and meets the needs of the application and its users. For esxample, if we pass `BiometricManager.Authenticators.BIOMETRIC_STRONG` constant as its parameter. This specifies that only strong biometric authentication methods (such as facial recognition and iris scanning) are allowed for use in the authentication prompt.

**Create Biometric Prompt**

add this function into class `BiometricHandler`:

```
fun createBiometricPrompt(): BiometricPrompt {
    val executor = ContextCompat.getMainExecutor(activity)
  
    // Callback
    val callback = object : BiometricPrompt.AuthenticationCallback() {
        override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
            super.onAuthenticationError(errorCode, errString)
            Timber.e("authentication error: $errorCode")
        }
   
        override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
            super.onAuthenticationSucceeded(result)
            Timber.e("authentication success")
        }
   
        override fun onAuthenticationFailed() {
            super.onAuthenticationFailed()
            Timber.e("authentication failed: unknown")
        }
   }
  
   return BiometricPrompt(activity, executor, callback)
}
```

in `onAuthenticationError` function, there is a parameter named “errorCode”, it contains:

*   **BIOMETRIC_ERROR_CANCELED**: The operation was canceled because the biometric sensor is unavailable.
*   **BIOMETRIC_ERROR_HW_NOT_PRESENT**: The device does not have a biometric sensor.
*   **BIOMETRIC_ERROR_HW_UNAVAILABLE**: The hardware is unavailable.
*   **BIOMETRIC_ERROR_LOCKOUT**: The operation was canceled because the API is locked out due to too many attempts.
*   **BIOMETRIC_ERROR_LOCKOUT_PERMANENT**: The operation was canceled because BIOMETRIC_ERROR_LOCKOUT occurred too many times.
*   **BIOMETRIC_ERROR_NO_BIOMETRICS**: The user does not have any biometrics enrolled.
*   **BIOMETRIC_ERROR_NO_DEVICE_CREDENTIAL**: The device does not have pin, pattern, or password set up.
*   **BIOMETRIC_ERROR_NO_SPACE**: Error state returned for operations like enrollment; the operation cannot be completed because there’s not enough storage remaining to complete the operation.
*   **BIOMETRIC_ERROR_SECURITY_UPDATE_REQUIRED**: A security vulnerability has been discovered and the sensor is unavailable until a security update has addressed this issue.
*   **BIOMETRIC_ERROR_TIMEOUT**: Error state returned when the current request has been running too long.
*   **BIOMETRIC_ERROR_UNABLE_TO_PROCESS**: Error state returned when the sensor was unable to process the current image.
*   **BIOMETRIC_ERROR_USER_CANCELED**: The user canceled the operation.
*   **BIOMETRIC_ERROR_VENDOR**: OEMs should use this constant if there are conditions that do not fit under any of the other publicly defined constants, and must provide appropriate strings for these errors to the `BiometricPrompt.AuthenticationCallback#onAuthenticationError(int, CharSequence)` callback.

**Show Biometric Prompt**

Finally, to display biometric authentication, add the function below:

```
fun showAuthentication(
    title: String,
    subtitle: String,
    description: String,
    negativeButtonText: String = "Cancel",
    allowedAuthenticators: Int = -1
) {
    createBiometricPrompt().authenticate(
        createPromptInfo(
            title = title, 
            subtitle = subtitle, 
            description = description, 
            negativeButtonText = negativeButtonText,
            allowedAuthenticators = allowedAuthenticators
        )
    )
}
``````
Button(
onClick = {
val canAuthenticate = BiometricHandler.canAuthenticateWithAuthenticators(
context = context,
authenticators = Authenticators.BIOMETRIC_WEAK
)

        if (canAuthenticate) {
            biometricHandler.showAuthentication(
                title = "Login using your fingerprint",
                subtitle = "Touch the fingerprint sensor",
                description = "To proceed, place your registered fingerprint on the sensor.",
                allowedAuthenticators = Authenticators.BIOMETRIC_WEAK
            )
        } else "Cannot authenticate".toast(context)
    },
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp)
) {
Text(
text = "Show biometric"
)
}
```

thank you for reading this article ♥