# cves
TESTING CVE's

Plugin: Meow Lightbox < 5.2.9
Affected Endpoint: /wp-json/meow-lightbox/v1/regenerate_mwl_data
Severity: High (CVSS ~7.5)
Access: Unauthenticated
Type: EXIF Metadata Disclosure via Insecure REST API
By Mrj Haxcore
🔥 Description:

The Meow Lightbox plugin exposes a REST API endpoint that allows unauthenticated users to submit image URLs from the site's media library and retrieve detailed metadata, including EXIF data (GPS, camera, timestamps), image dimensions, and internal attachment IDs.

The endpoint lacks proper access controls (__return_true as the permission callback), making it publicly accessible.

✅ PoC:

POST /wp-json/meow-lightbox/v1/regenerate_mwl_data
Content-Type: application/json

{
  "images": [
    { "url": "https://target.com/wp-content/uploads/2025/06/image.jpg" }
  ]
}

🔐 Recommendation:

Restrict the endpoint using:

'permission_callback' => function() {
  return current_user_can('upload_files');
};
