import xmltodict
data = {'output':{
      "video_path": "./awesome.mp4",
      "video_type": ".mp4",
      "video_width": 640,
      "video_height": 480,
      "video_frame_rate": 30,
      "vehicles_detected":
      [
          {
              "frame_id": 10,
              "vehicles":
              [
                  {
                    "vehicle_id": 0,
                    "vehicle_xywh":
                    [
                        23,
                        45,
                        46,
                        22
                    ],
                      "license_plate":
                      {
                        "lp_xywh":
                        [
                            32,
                            55,
                            16,
                            12
                        ],
                        "ocr": "B2233XFS",
                        "ocr_conf": 0.9567
                    }
                  }
              ]
          },
          {
              "frame_id": 13,
              "vehicles":
              [
                  {
                      "vehicle_id": 1,
                      "vehicle_xywh":
                      [
                          25,
                          49,
                          44,
                          18
                      ],
                      "license_plate":
                      {
                          "lp_xywh":
                          [
                              36,
                              51,
                              19,
                              14
                          ],
                          "ocr": "D3432DFE",
                          "ocr_conf": 0.8456
                      }
                  },
                  {
                      "vehicle_id": 2,
                      "vehicle_xywh":
                      [
                          25,
                          49,
                          44,
                          18
                      ],
                      "license_plate":
                      {
                          "lp_xywh":
                          [
                              36,
                              51,
                              19,
                              14
                          ],
                          "ocr": "",
                      }
                  },
                  {
                      "vehicle_id": 3,
                      "vehicle_xywh":
                      [
                          25,
                          49,
                          44,
                          18
                      ],
                      "license_plate":
                      {}
                  }
              ]
          }
      ]
  }
}

xml = xmltodict.unparse(data,pretty=True)

wfile = open('yourxmlfileoutput.xml','w')
wfile.write(xml)
wfile.close()