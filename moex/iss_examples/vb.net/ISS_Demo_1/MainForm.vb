Imports System.Net
Imports System.IO

Imports ISS_Demo.MicexAuth
Imports ISS_Demo.MicexISSClient
Imports ISS_Demo.MicexISSDataHandler

Public Class MainForm
    Dim MyAuth As MicexAuth
    Dim MyClient As MicexISSClient
    Dim MyHandler As New MicexISSDataHandler

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        DateTimePicker1.Value = Today().AddDays(-1)
    End Sub

    Private Sub btn_get_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_get.Click
        ' get the historical data only when there's a valid authentication cookie
        ' would not be required for indices and for the delayed intraday market data
        If MyAuth Is Nothing Then
            MsgBox("You need to authenticate in order to access the historical data")
            Return
        End If
        If MyAuth.IsRealTime() = False Then
            MsgBox("Cannot access real-time and historical data. Try to reauthenticate.")
            Return
        End If

        ResultGrid.Rows.Clear()

        Dim iss_date As String = String.Format("{0}-{1}-{2}", DateTimePicker1.Value.Year.ToString, DateTimePicker1.Value.Month.ToString, DateTimePicker1.Value.Day.ToString)

        If Not MyClient Is Nothing Then
            ' get the user's choice from the screen form
            Dim engine_name As String = GetSelectedEngine()
            Dim market_name As String = GetSelectedMarket()
            Dim board_id As String = GetSelectedBoard()

            If (Len(engine_name) > 0) And (Len(market_name) > 0) And (Len(board_id) > 0) Then
                MyClient.GetHistorySecurities(engine_name, market_name, board_id, iss_date, MyHandler)
                For Each row In MyHandler.history_storage
                    Dim myrow As String() = {row(0).ToString, row(1).ToString, row(2).ToString}
                    ResultGrid.Rows.Add(myrow)
                Next
            End If
        Else
            MsgBox("MyClient object instance is not initialized")
        End If
    End Sub

    Private Sub btn_auth_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_auth.Click
        ' perform one attempt to authenticate
        MyAuth = New MicexAuth(txt_username.Text, txt_password.Text)
        Dim st As String = "Result:"
        st = st & vbCrLf & "Status Code: " & MyAuth.last_status
        st = st & vbCrLf & "Status Text: " & MyAuth.last_status_text
        st = st & vbCrLf & "Real-time: " & MyAuth.IsRealTime()
        txt_auth.Text = st
        If MyAuth.last_status = HttpStatusCode.OK Then
            If listbox_board.SelectedItems.Count = 1 Then btn_get.Enabled = True
            MyClient = New MicexISSClient(MyAuth.cookiejar)
        Else
            btn_get.Enabled = False
        End If
    End Sub

    Private Sub btn_engines_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_engines.Click
        ' get the initial list of engines from the ISS server
        ' we do not care about cookies here because general data is always available to everyone
        If MyClient Is Nothing Then MyClient = New MicexISSClient()
        btn_get.Enabled = False
        listbox_engine.Items.Clear()
        MyClient.GetEngines(MyHandler)
        For Each row In MyHandler.engines_storage
            listbox_engine.Items.Add(row.Value.ToString)
        Next
    End Sub

    Private Sub listbox_engine_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles listbox_engine.SelectedIndexChanged
        ' user has chosen another engine
        listbox_market.Items.Clear()
        listbox_board.Items.Clear()
        btn_get.Enabled = False
        If listbox_engine.SelectedItems.Count <> 1 Then Exit Sub
        Dim engine_name As String = GetSelectedEngine()
        If Len(engine_name) > 0 Then
            MyClient.GetMarkets(engine_name, MyHandler)
            For Each row In MyHandler.markets_storage
                listbox_market.Items.Add(row.Value.ToString)
            Next
        End If
    End Sub

    Private Sub listbox_board_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles listbox_board.SelectedIndexChanged
        ' user has selected a board - the last required parameter
        If (listbox_board.Items.Count > 0) And (Not MyAuth Is Nothing) Then
            If MyAuth.last_status = HttpStatusCode.OK Then btn_get.Enabled = True
        End If
    End Sub

    Private Sub listbox_market_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles listbox_market.SelectedIndexChanged
        ' user has chosen another market
        listbox_board.Items.Clear()
        btn_get.Enabled = False
        If listbox_market.SelectedItems.Count <> 1 Then Exit Sub
        Dim engine_name As String = GetSelectedEngine()
        If Len(engine_name) > 0 Then
            Dim market_name As String = GetSelectedMarket()
            If Len(market_name) > 0 Then
                MyClient.GetBoards(engine_name, market_name, MyHandler)
                For Each row In MyHandler.boards_storage
                    listbox_board.Items.Add(row.Value.ToString)
                Next
            End If
        End If
    End Sub

    Private Function GetSelectedEngine() As String
        ' read the user's selection of engine from the screen form
        Dim engine_name As String = ""
        If listbox_engine.SelectedItems.Count = 1 Then
            For Each row In MyHandler.engines_storage
                If row.Value = listbox_engine.SelectedItem.ToString Then
                    engine_name = row.Key.ToString
                    Exit For
                End If
            Next
        End If
        Return engine_name
    End Function

    Private Function GetSelectedMarket() As String
        ' read the user's selection of market from the screen form
        Dim market_name As String = ""
        If listbox_market.SelectedItems.Count = 1 Then
            For Each row In MyHandler.markets_storage
                If row.Value = listbox_market.SelectedItem.ToString Then
                    market_name = row.Key.ToString
                    Exit For
                End If
            Next
        End If
        Return market_name
    End Function

    Private Function GetSelectedBoard() As String
        ' read the user's selection of board from the screen form
        Dim board_id As String = ""
        If listbox_board.SelectedItems.Count = 1 Then
            For Each row In MyHandler.boards_storage
                If row.Value = listbox_board.SelectedItem.ToString Then
                    board_id = row.Key.ToString
                    Exit For
                End If
            Next
        End If
        Return board_id
    End Function

End Class
