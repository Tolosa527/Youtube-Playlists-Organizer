SPREADSHEET_ID = "YOUR SPREADSHEET ID"

function get_videos(playlistId) {
  videos = []
  do {
    var next_page_token = playlistResponse != null ? playlistResponse.nextPageToken : ""
    var playlistResponse = YouTube.PlaylistItems.list('contentDetails, snippet', {
          playlistId: playlistId,
          maxResults: 20,
          pageToken: next_page_token
        });
    playlistResponse.items.forEach(item => {
      videos.push(
        [
          `https://www.youtube.com/watch?v=${item.contentDetails.videoId}`,
          item.snippet.title,
          item.snippet.publishedAt
        ]
      )
    })
  } while (playlistResponse.nextPageToken != null)
  return videos
}

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  // Or DocumentApp or FormApp.
  ui.createMenu('Custom Menu')
      .addItem('Import from youtube', "videosImporter")
      .addToUi();
}

function videosImporter() {
  var ui = SpreadsheetApp.getUi();
  var playlistId = ui.prompt("Paste playlist ID", )
  var table = SpreadsheetApp.openById(SPREADSHEET_ID).getActiveSheet()
  Logger.log(playlistId.getResponseText)
  var videos = get_videos(playlistId.getResponseText())
  var row_len = videos.length
  var tableRange = table.getRange(2, 5, row_len, 3)
  tableRange.setValues(videos)
}

function main(playlistId){
  var videos = get_videos(playlistId);
  var videos_obj = []
  videos.forEach((video)=>{
      videos_obj.push(
        {
          "url":video[0],
          "name":video[1],
          "upload_at":video[2] 
        }
      )
    }
  )
  return videos_obj
}

function doPost(e){
  return ContentService.createTextOutput(
    JSON.stringify(
      main(e.parameter.playlist_id)
    )
  )
}