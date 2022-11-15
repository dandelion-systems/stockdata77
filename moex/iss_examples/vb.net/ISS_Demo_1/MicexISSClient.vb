Imports System.Net
Imports System.IO
Imports System.Xml.Linq
Imports ISS_Demo.MicexISSDataHandler

' class to perform all the interaction with the ISS server
Public Class MicexISSClient
    ' container for all the cookies
    Private cookiejar As CookieContainer
    ' dictionary with all the URLs that can be used to request data from the ISS
    Private urls As New Dictionary(Of String, String)

    Public Sub New(Optional ByVal cookies As CookieContainer = Nothing)
        cookiejar = cookies
        urls.Add("history_secs", "http://iss.moex.com/iss/history/engines/{0}/markets/{1}/boards/{2}/securities.xml?date={3}&start={4}")
        urls.Add("engines", "http://iss.moex.com/iss/engines.xml")
        urls.Add("markets", "http://iss.moex.com/iss/engines/{0}/markets.xml")
        urls.Add("boards", "http://iss.moex.com/iss/engines/{0}/markets/{1}/boards.xml")
    End Sub

    Private Function GetReply(ByVal url As String) As String
        ' get raw reply from ISS as a string
        Try
            Dim MyWebRequest As HttpWebRequest
            MyWebRequest = HttpWebRequest.Create(url)
            MyWebRequest.CookieContainer = cookiejar
            Dim ISSResponse As HttpWebResponse
            ISSResponse = DirectCast(MyWebRequest.GetResponse(), HttpWebResponse)
            Dim MyReplyStream As Stream
            MyReplyStream = ISSResponse.GetResponseStream()
            Dim MyStreamReader As New StreamReader(MyReplyStream)
            Dim ret As String = ""
            ret = MyStreamReader.ReadToEnd()
            ISSResponse.Close()
            Return ret
        Catch e As Exception
            MsgBox("Error requesting data: ", e.Message.ToString)
            Return ""
        End Try
    End Function

    Private Function GetDataBlock(ByVal resXML As XDocument, ByVal block_id As String) As XElement
        ' get a particular data block from ISS XML reply
        Dim att As XAttribute
        Dim ret As XElement = <data id="none"></data>
        For Each el In resXML.Element("document").Elements()
            att = el.Attribute("id")
            If (Not att Is Nothing) Then
                If att.Value.ToString = block_id Then
                    ret = el
                    Exit For
                End If
            End If
        Next
        Return ret
    End Function

    Private Function GetRows(ByVal elem As XElement) As XElement
        ' get a set of rows inside a data block in the ISS XML
        Dim ret As XElement = <rows></rows>
        For Each el In elem.Elements()
            If el.Name = "rows" Then
                ret = el
                Exit For
            End If
        Next
        Return ret
    End Function

    Private Function GetAttribute(ByVal elem As XElement, ByVal attr As String) As String
        ' get a particular attribute of an element
        ' this is not the best solution when a lot of attributes from a single element are to be extracted
        Dim ret As String = ""
        For Each att In elem.Attributes()
            If Strings.UCase(att.Name.ToString) = Strings.UCase(attr) Then
                ret = att.Value.ToString
                Exit For
            End If
        Next
        Return ret
    End Function

    Public Sub GetHistorySecurities(ByVal engine As String, ByVal market As String, ByVal board As String, ByVal histdate As String, ByRef myhandler As MicexISSDataHandler)
        ' full cycle to get the end-of-day results
        ' only Security ID, number of trades and the official close price are stored in this example
        Dim start As Integer = 0
        Dim reply_len As Integer = 1
        Dim reply As String = ""
        Dim secid As String = ""
        Dim closeprice# = 0.0
        Dim numtrades As UInteger = 0
        Dim history As XElement
        Dim rows As XElement
        Dim fullurl As String
        myhandler.history_storage = New Collection()
        Try
            ' it is very important to keep in mind that the server reply can be split into serveral pages,
            ' so we use the 'start' argument to the request
            While reply_len > 0
                reply_len = 0

                fullurl = String.Format(urls.Item("history_secs"), engine, market, board, histdate, start.ToString)
                reply = GetReply(fullurl)

                ' get the data block with historical data
                ' we ignore metadata in this example
                history = GetDataBlock(XDocument.Parse(reply), "history")
                If history.HasElements() Then
                    rows = GetRows(history)
                    If rows.HasElements Then
                        For Each el In rows.Elements()
                            secid = GetAttribute(el, "SECID")
                            numtrades = GetAttribute(el, "NUMTRADES")
                            ' need to use Val instead of Convert or CDbl, because the ISS float numbers always come with . as the delimiter
                            closeprice = Val(GetAttribute(el, "LEGALCLOSEPRICE"))
                            myhandler.process_history(secid, closeprice, numtrades)
                        Next
                        reply_len = rows.Elements().Count
                    End If
                End If
                start = start + reply_len
            End While
        Catch e As Exception
            MsgBox("Error while processing XML with history_secs: " & e.Message.ToString)
        End Try
    End Sub

    Public Sub GetEngines(ByRef myhandler As MicexISSDataHandler)
        ' the the list of available engines
        myhandler.engines_storage = New Dictionary(Of String, String)
        Try
            Dim reply As String = GetReply(urls.Item("engines"))
            Dim engines As XElement = GetDataBlock(XDocument.Parse(reply), "engines")
            If engines.HasElements() Then
                Dim rows As XElement = GetRows(engines)
                If rows.HasElements Then
                    For Each el In rows.Elements()
                        myhandler.process_engines(GetAttribute(el, "name"), GetAttribute(el, "title"))
                    Next
                End If
            End If
        Catch e As Exception
            MsgBox("Error while processing XML with engines: " & e.Message.ToString)
        End Try
    End Sub

    Public Sub GetMarkets(ByVal engine_name As String, ByRef myhandler As MicexISSDataHandler)
        ' get the list of markets on a given engine
        myhandler.markets_storage = New Dictionary(Of String, String)
        Try
            Dim reply As String = GetReply(String.Format(urls.Item("markets"), engine_name))
            Dim markets As XElement = GetDataBlock(XDocument.Parse(reply), "markets")
            If markets.HasElements() Then
                Dim rows As XElement = GetRows(markets)
                If rows.HasElements Then
                    For Each el In rows.Elements()
                        myhandler.process_markets(GetAttribute(el, "name"), GetAttribute(el, "title"))
                    Next
                End If
            End If
        Catch e As Exception
            MsgBox("Error while processing XML with markets: " & e.Message.ToString)
        End Try
    End Sub

    Public Sub GetBoards(ByVal engine_name As String, ByVal market_name As String, ByRef myhandler As MicexISSDataHandler)
        ' get the list of boards on a given engine and a given market
        myhandler.boards_storage = New Dictionary(Of String, String)
        Try
            Dim reply As String = GetReply(String.Format(urls.Item("boards"), engine_name, market_name))
            Dim boards As XElement = GetDataBlock(XDocument.Parse(reply), "boards")
            If boards.HasElements() Then
                Dim rows As XElement = GetRows(boards)
                If rows.HasElements Then
                    For Each el In rows.Elements()
                        myhandler.process_boards(GetAttribute(el, "boardid"), GetAttribute(el, "title"))
                    Next
                End If
            End If
        Catch e As Exception
            MsgBox("Error while processing XML with boards: " & e.Message.ToString)
        End Try
    End Sub

End Class
