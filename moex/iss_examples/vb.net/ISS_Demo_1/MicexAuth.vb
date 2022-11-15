Imports System.Net
Imports System.IO

' Class with ISS authentication functions and data
Public Class MicexAuth
    ' MICEX Passport username
    Private username As String
    ' MICEX Passport password
    Private password As String

    ' Storage for all cookies which will be submitted with further requests
    Public cookiejar As New CookieContainer()
    ' Separate storage for a passport cookie, just for convenience
    Public passport As New Cookie()

    ' HTTP status
    ' will be set to BadRequest for non-protocol errors
    Public last_status As HttpStatusCode
    Public last_status_text As String
    'Public headers As New WebHeaderCollection()

    ' URL for authorization in order to get a passport cookie
    Public url_auth = "https://passport.moex.com/authenticate"
    ' URL that will be used as URI to find a cookie for the correct domain
    Public url_uri = "http://moex.com"

    Public Sub New(ByVal user_name As String, ByVal passwd As String)
        username = user_name
        password = passwd
        Auth()
    End Sub

    Public Sub Auth()
        Try
            Dim AuthReq As HttpWebRequest = CType(WebRequest.Create(url_auth), HttpWebRequest)
            Dim AuthResponse As HttpWebResponse
            AuthReq.CookieContainer = New CookieContainer()

            ' use the Basic authorization mechanism
            Dim binData() As Byte
            binData = System.Text.Encoding.UTF8.GetBytes(username & ":" & password)
            Dim sAuth64 As String = Convert.ToBase64String(binData, System.Base64FormattingOptions.None)
            AuthReq.Headers.Add(HttpRequestHeader.Authorization, "Basic " & sAuth64)

            AuthResponse = CType(AuthReq.GetResponse(), HttpWebResponse)
            AuthResponse.Close()
            last_status = AuthResponse.StatusCode()

            cookiejar = New CookieContainer()
            cookiejar.Add(AuthResponse.Cookies)

            ' find the Passport cookie for a given domain URI
            Dim myuri As New System.Uri(url_uri)
            Dim cook As Cookie
            passport = New Cookie()
            For Each cook In cookiejar.GetCookies(myuri)
                If cook.Name() = "MicexPassportCert" Then passport = cook
            Next
            If passport.Name <> "MicexPassportCert" Then
                last_status_text = "Passport cookie not found"
            Else
                last_status_text = "OK"
            End If

        Catch e As WebException
            Console.WriteLine(e.Message)
            If e.Status = WebExceptionStatus.ProtocolError Then
                Console.WriteLine("Status Code : {0}", CType(e.Response, HttpWebResponse).StatusCode)
                Console.WriteLine("Status Description : {0}", CType(e.Response, HttpWebResponse).StatusDescription)
                last_status = CType(e.Response, HttpWebResponse).StatusCode
                last_status_text = CType(e.Response, HttpWebResponse).StatusDescription
            Else
                last_status = HttpStatusCode.BadRequest
                last_status_text = e.Message
            End If

        Catch e As Exception
            Console.WriteLine(e.Message)
            last_status = HttpStatusCode.BadRequest
            last_status_text = e.Message
        End Try
    End Sub

    Public Function IsRealTime() As Boolean
        ' repeat authorization request if failed last time or if the Passport has expired
        If (passport Is Nothing) Or ((Not passport Is Nothing) And (passport.Expired)) Then Auth()
        If (Not passport Is Nothing) And (Not passport.Expired) And (passport.Name = "MicexPassportCert") Then Return True
        Return False
    End Function

End Class
