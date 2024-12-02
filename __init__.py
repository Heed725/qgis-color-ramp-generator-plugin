def classFactory(iface):
    from .plugin import QGISColorRampGenerator
    return QGISColorRampGenerator(iface)
