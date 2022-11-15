Imports System

' class to process and store data that is being downloaded from the ISS server
Public Class MicexISSDataHandler
    Public history_storage As New Collection()
    Public engines_storage As New Dictionary(Of String, String)
    Public markets_storage As New Dictionary(Of String, String)
    Public boards_storage As New Dictionary(Of String, String)

    Public Sub process_history(ByVal secid As String, ByVal closeprice As Double, ByVal numtrades As UInteger)
        ' for the requests of historical end-of-day results
        Dim row() = {secid, closeprice, numtrades}
        history_storage.Add(row)
    End Sub

    Public Sub process_engines(ByVal engine_name As String, ByVal engine_title As String)
        ' for the request of the list of engies
        engines_storage.Add(engine_name, engine_title)
    End Sub

    Public Sub process_markets(ByVal market_name As String, ByVal market_title As String)
        ' for the request of the list of markets on a given engine
        markets_storage.Add(market_name, market_title)
    End Sub

    Public Sub process_boards(ByVal board_id As String, ByVal board_title As String)
        ' for the request of the list of boards on a given engine and a given market
        boards_storage.Add(board_id, board_title)
    End Sub
End Class
